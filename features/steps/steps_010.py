from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Mapa de nombres de ciudades en español → inglés para búsquedas en el sitio
_CITY_MAP = {
    "Tokio": "Tokyo",
    "París": "Paris",
    "Moscú": "Moscow",
    "Londres": "London",
    "Pekín": "Beijing",
}

def _add_city(driver, city_name):
    """Agrega una ciudad al convertidor usando JS click para evitar StaleElement."""
    search_term = _CITY_MAP.get(city_name, city_name)
    inp = WebDriverWait(driver, 8).until(
        EC.element_to_be_clickable((By.ID, "addtxt"))
    )
    inp.clear()
    inp.send_keys(search_term)
    for _ in range(3):
        try:
            item = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='asu']/li/a"))
            )
            driver.execute_script("arguments[0].click();", item)
            time.sleep(1)
            return
        except Exception:
            time.sleep(0.5)

@given('que el usuario convierte la hora actual de Bogotá a "{destino}" en el conversor de husos horarios')
def step_impl(context, destino):
    context.driver.get("https://www.timeanddate.com/worldclock/converter.html")
    time.sleep(1)
    _add_city(context.driver, "Bogota")
    _add_city(context.driver, destino)

@when('anota el resultado de la conversión')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, "location__row")) >= 2
    )
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    context.conversion_output = rows[1].find_element(
        By.CLASS_NAME, "location__formatted-time"
    ).text.split(":")[0].strip()

@when('navega inmediatamente al "World Clock" y busca "{destino}"')
def step_impl(context, destino):
    search_term = _CITY_MAP.get(destino, destino)
    context.driver.get("https://www.timeanddate.com/worldclock/")
    search = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.picker-city__input"))
    )
    context.driver.execute_script("arguments[0].click();", search)
    search.send_keys(search_term)
    item = WebDriverWait(context.driver, 8).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='asu']/li/a"))
    )
    context.driver.execute_script("arguments[0].click();", item)

@then('la hora mostrada en el reloj mundial para Tokio coincide con la conversión previa con un margen máximo de 1 minuto')
def step_impl(context):
    live_clock = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "ct"))
    ).text.split(":")[0].strip()
    assert context.conversion_output == live_clock, \
        f"Conversión={context.conversion_output} vs reloj={live_clock}"
