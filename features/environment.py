import atexit
import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

_HTML_REPORT = "reporte_pruebas.html"

# Cookies de sesión compartidas — login ocurre UNA SOLA VEZ en before_all
_SESSION_COOKIES = None


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
        "  img[id^='embed_'] { display: block !important; max-width: 100%; margin: 6px 0; border: 1px solid #ccc; }\n"
        "  pre[id^='embed_'] { display: block !important; background: #f5f5f5; padding: 8px; white-space: pre-wrap; }\n"
        "  video[id^='embed_'] { display: block !important; max-width: 100%; }\n"
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
    """Login único — guarda cookies para reuso en escenarios que necesiten sesión."""
    global _SESSION_COOKIES
    driver = _make_driver(incognito=False)
    try:
        driver.get("https://www.timeanddate.com/custom/login.html")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys("kev082001@gmail.com")
        driver.find_element(By.ID, "password").send_keys("285285Ok")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(driver, 20).until(lambda d: "login" not in d.current_url)
        time.sleep(1)
        _SESSION_COOKIES = driver.get_cookies()
        print(f"\n[AUTH] Sesión establecida — {len(_SESSION_COOKIES)} cookies guardadas.")
    except Exception as e:
        print(f"\n[AUTH] No se pudo hacer login previo: {e}")
        _SESSION_COOKIES = []
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
    # Exponer inject_session para que los steps puedan usarlo
    context.inject_session = lambda: inject_session(context.driver)

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
