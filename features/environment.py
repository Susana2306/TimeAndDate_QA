import atexit
import os
import sys
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

_HTML_REPORT = "reporte_pruebas.html"

# Resultados de escenarios: { 'U-13.1': { status, scenario_name, error_msg } }
_test_results = {}

# Cookies de sesión compartidas — login ocurre UNA SOLA VEZ en before_all
_SESSION_COOKIES = None

# Credenciales: se intenta en orden, la primera que funcione queda activa
_CREDENTIALS = [
    ("lupitasolorzanosalazar@gmail.com", "Susana12345678"),
    ("kev082001@gmail.com", "285285Ok"),
]
_ACTIVE_CREDS = _CREDENTIALS[0]  # fallback por defecto


def _expand_embeds():
    """Post-procesa el HTML para mostrar capturas expandidas sin necesidad de click."""
    if not os.path.exists(_HTML_REPORT):
        return
    with open(_HTML_REPORT, "r", encoding="utf-8") as f:
        content = f.read()
    if "</body>" not in content:
        return
    css = (
        "<style>\n"
        "  span.embed { display: block; }\n"
        "  img[id^='embed_'] { display: inline-block !important; width: calc(50% - 6px); max-width: calc(50% - 6px); vertical-align: top; box-sizing: border-box; margin: 3px; border: 1px solid #ccc; }\n"
        "  pre[id^='embed_'] { display: block !important; background: #f5f5f5; padding: 8px; white-space: pre-wrap; box-sizing: border-box; }\n"
        "  video[id^='embed_'] { display: inline-block !important; width: calc(50% - 6px); max-width: calc(50% - 6px); vertical-align: top; box-sizing: border-box; margin: 3px; }\n"
        "</style>"
    )
    content = content.replace("</body>", css + "\n</body>", 1)
    with open(_HTML_REPORT, "w", encoding="utf-8") as f:
        f.write(content)


atexit.register(_expand_embeds)


def _make_driver(incognito=True):
    options = webdriver.ChromeOptions()
    if incognito:
        options.add_argument("--incognito")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(8)
    return driver


def before_all(context):
    """Login único — prueba credenciales en orden, guarda cookies de la primera que funcione."""
    global _SESSION_COOKIES, _ACTIVE_CREDS
    driver = _make_driver(incognito=False)
    try:
        for email, password in _CREDENTIALS:
            try:
                driver.get("https://www.timeanddate.com/custom/login.html")
                time.sleep(2)
                driver.find_element(By.ID, "email").clear()
                driver.find_element(By.ID, "email").send_keys(email)
                driver.find_element(By.ID, "password").clear()
                driver.find_element(By.ID, "password").send_keys(password)
                driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
                WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url)
                time.sleep(1)
                _SESSION_COOKIES = driver.get_cookies()
                _ACTIVE_CREDS = (email, password)
                print(f"\n[AUTH] Sesión establecida con {email} — {len(_SESSION_COOKIES)} cookies guardadas.")
                break
            except Exception as e:
                print(f"\n[AUTH] Falló con {email}: {e}. Intentando siguiente...")
                _SESSION_COOKIES = []
        else:
            print("\n[AUTH] Todas las credenciales fallaron.")
    finally:
        driver.quit()


def inject_session(driver):
    """Inyecta las cookies de sesión en el driver activo."""
    if not _SESSION_COOKIES:
        return
    driver.get("https://www.timeanddate.com")
    time.sleep(1)
    for cookie in _SESSION_COOKIES:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
    driver.refresh()
    time.sleep(1)


def before_scenario(context, scenario):
    context.driver = _make_driver(incognito=True)
    context.inject_session = lambda: inject_session(context.driver)
    context.credentials = _ACTIVE_CREDS  # (email, password) de la sesión activa

    # Conectar context.embed al formatter HTML si está activo
    context.embed = None
    for formatter in context._runner.formatters:
        if hasattr(formatter, "embedding"):
            context.embed = formatter.embedding
            break


def _embed_screenshot(context, caption):
    """Toma pantallazo y lo embebe en el reporte HTML."""
    if not hasattr(context, "driver") or context.embed is None:
        return
    try:
        b64 = context.driver.get_screenshot_as_base64()
        context.embed("image/png", b64, caption)
    except Exception:
        pass


def after_step(context, step):
    if step.status == "failed":
        _embed_screenshot(context, f"Fallo en: {step.name}")
        if context.embed is not None and step.exception is not None:
            tb_lines = traceback.format_exception(
                type(step.exception), step.exception, step.exc_traceback
            )
            context.embed("text/plain", "".join(tb_lines), "Detalle del Error")
    else:
        _embed_screenshot(context, f"Paso OK: {step.name}")


def after_scenario(context, scenario):
    global _test_results

    if hasattr(context, "driver"):
        estado = "PASÓ" if scenario.status == "passed" else "FALLÓ"
        _embed_screenshot(context, f"Estado final [{estado}]")

        if scenario.status == "failed":
            os.makedirs("evidencias_fallas", exist_ok=True)
            nombre_archivo = scenario.name.replace(" ", "_").lower()
            ruta = f"evidencias_fallas/{nombre_archivo}.png"
            context.driver.save_screenshot(ruta)
            print(f"\n[ALERTA QA] Escenario fallido. Captura guardada en: {ruta}")

        context.driver.quit()

    # Colectar resultado para actualización de Excel
    error_msg = None
    if scenario.status == "failed":
        for step in scenario.steps:
            if step.status == "failed" and step.exception:
                error_msg = f"Fallo en '{step.name}': {step.exception}"
                break

    for tag in scenario.tags:
        # Solo tags que corresponden a IDs de casos (U-X.Y, P-X.Y, E-X.Y, I-X.Y)
        if len(tag) > 2 and tag[1] == "-" and tag[0].isalpha():
            _test_results[tag] = {
                "status": str(scenario.status),
                "scenario_name": scenario.name,
                "error_msg": error_msg,
            }


def after_all(context):
    if not _test_results:
        return
    # Asegurar que update_excel_results.py sea encontrado desde cualquier cwd
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from update_excel_results import update_excel
        update_excel(_test_results)
    except Exception as e:
        print(f"\n[EXCEL] Error al actualizar el Excel: {e}")
