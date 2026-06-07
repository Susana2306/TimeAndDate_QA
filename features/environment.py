import atexit
import os
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

_HTML_REPORT = "reporte_pruebas.html"


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


def before_scenario(context, scenario):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.implicitly_wait(8)

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
        # Pantallazo en el paso que falló
        _embed_screenshot(context, f"Fallo en: {step.name}")

        # Detalle completo del error (traceback)
        if context.embed is not None and step.exception is not None:
            tb_lines = traceback.format_exception(
                type(step.exception), step.exception, step.exc_traceback
            )
            context.embed("text/plain", "".join(tb_lines), "Detalle del Error")
    else:
        # Pantallazo de cada paso exitoso (muestra progresión)
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