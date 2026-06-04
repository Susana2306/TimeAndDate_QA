import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def before_scenario(context, scenario):
    """
    Este bloque se ejecuta AUTOMÁTICAMENTE ANTES de que empiece 
    cada escenario individual de tus carpetas ESC_XXX.
    """
    # 1. Configurar opciones de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")  # Bloquea ventanas emergentes molestas
    # options.add_argument("--headless") # Descomenta esta línea si no quieres ver el navegador abrirse (Modo oculto)

    # 2. Inicializar el WebDriver de Selenium con WebDriver Manager
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

    # 3. Configurar un tiempo de espera implícito global (8 segundos)
    # Si Selenium no encuentra un elemento en timeanddate.com, esperará hasta 8s antes de lanzar error.
    context.driver.implicitly_wait(8)


def after_scenario(context, scenario):
    """
    Este bloque se ejecuta AUTOMÁTICAMENTE DESPUÉS de que termina 
    cada escenario (ya sea que haya pasado con éxito o haya fallado).
    """
    # 4. CONTROL DE ERRORES: Si la ruta (crítica o alterna) falla, toma una foto de la pantalla
    if scenario.status == "failed":
        # Crea una carpeta de evidencias si no existe
        os.makedirs("evidencias_fallas", exist_ok=True)
        
        # Define el nombre del archivo según el nombre de tu escenario en Gherkin
        nombre_archivo = scenario.name.replace(" ", "_").lower()
        ruta_screenshot = f"evidencias_fallas/{nombre_archivo}.png"
        
        # Guarda la captura de pantalla
        context.driver.save_screenshot(ruta_screenshot)
        print(f"\n[ALERTA QA] Escenario fallido. Captura de pantalla guardada en: {ruta_screenshot}")

    # 5. Cierre seguro del navegador para liberar memoria RAM
    if hasattr(context, 'driver'):
        context.driver.quit()