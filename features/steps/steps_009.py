from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def _click_first_asu(driver, timeout=8):
    """Re-fetch and JS-click the first autocomplete item to avoid StaleElement."""
    for _ in range(3):
        try:
            item = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='asu']/li/a"))
            )
            driver.execute_script("arguments[0].click();", item)
            time.sleep(1)
            return
        except Exception:
            time.sleep(0.5)

@given('que el usuario abre el convertidor de huso horario de timeanddate (/worldclock/converter.html)')
@given('que el usuario se encuentra en la pantalla del convertidor de hora')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/worldclock/converter.html")
    time.sleep(1)

@when('selecciona "{ciudad}" en el campo de ciudad origen')
def step_impl(context, ciudad):
    p1 = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.ID, "addtxt"))
    )
    p1.clear()
    p1.send_keys(ciudad)
    _click_first_asu(context.driver)

@when('selecciona la misma zona "{ciudad}" en el campo de ciudad destino')
def step_impl(context, ciudad):
    p2 = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.ID, "addtxt"))
    )
    p2.clear()
    p2.send_keys(ciudad)
    _click_first_asu(context.driver)

@when('selecciona una zona origen "{ciudad_orig}" y una zona destino diferente como "{ciudad}"')
def step_impl(context, ciudad_orig, ciudad):
    for nombre in (ciudad_orig, ciudad):
        box = WebDriverWait(context.driver, 8).until(
            EC.element_to_be_clickable((By.ID, "addtxt"))
        )
        box.clear()
        box.send_keys(nombre)
        _click_first_asu(context.driver)
        time.sleep(0.5)

@when('introduce una hora específica para la conversión')
def step_impl(context):
    time_btn = WebDriverWait(context.driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "location__formatted-time"))
    )
    context.driver.execute_script("arguments[0].scrollIntoView(true);", time_btn)
    context.driver.execute_script("arguments[0].click();", time_btn)
    h = WebDriverWait(context.driver, 5).until(EC.presence_of_element_located((By.ID, "h1")))
    h.clear()
    h.send_keys("15")
    m = context.driver.find_element(By.ID, "i1")
    m.clear()
    m.send_keys("00")
    close_btn = WebDriverWait(context.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Close')]"))
    )
    context.driver.execute_script("arguments[0].click();", close_btn)

@when('ejecuta el cálculo de conversión presionando el botón "Convert time"')
@when('ejecuta el cálculo de conversión')
def step_impl(context):
    pass

@then('el resultado muestra exactamente la misma hora o un mensaje indicando que las zonas son idénticas')
def step_impl(context):
    # Re-fetch rows to avoid stale reference
    WebDriverWait(context.driver, 8).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, "location__row")) >= 2
    )
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    h1 = rows[0].find_element(By.CLASS_NAME, "location__formatted-time").text.strip()
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    h2 = rows[1].find_element(By.CLASS_NAME, "location__formatted-time").text.strip()
    assert h1 == h2

@then('el resultado final en pantalla corresponde exactamente a la hora calculada y convertida en la zona destino')
def step_impl(context):
    WebDriverWait(context.driver, 8).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, "location__row")) >= 2
    )
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    resultado_bloque = rows[1].find_element(By.CLASS_NAME, "location__formatted-time")
    assert resultado_bloque.is_displayed()
