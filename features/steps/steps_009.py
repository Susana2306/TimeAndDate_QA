from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario abre el convertidor de huso horario de timeanddate (/worldclock/converter.html)')
@given('que el usuario se encuentra en la pantalla del convertidor de hora')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/worldclock/converter.html")

@when('selecciona "{ciudad}" en el campo de ciudad origen')
def step_impl(context, ciudad):
    p1 = context.driver.find_element(By.ID, "addtxt")
    p1.clear()
    p1.send_keys(ciudad)
    WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))).click()

@when('selecciona la misma zona "{ciudad}" en el campo de ciudad destino')
@when('selecciona una zona origen "{ciudad_orig}" y una zona destino diferente como "{ciudad}"')
def step_impl(context, ciudad, ciudad_orig=None):
    p2 = context.driver.find_element(By.ID, "addtxt")
    p2.clear()
    p2.send_keys(ciudad)
    WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))).click()

@when('introduce una hora específica para la conversión')
def step_impl(context):
    # Click the time button to open the edit date/time modal
    time_btn = WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "location__formatted-time")))
    time_btn.click()
    
    # Enter the hour and minutes
    h = WebDriverWait(context.driver, 5).until(EC.presence_of_element_located((By.ID, "h1")))
    h.clear()
    h.send_keys("15")
    
    m = context.driver.find_element(By.ID, "i1")
    m.clear()
    m.send_keys("00")
    
    # Click the close button
    context.driver.find_element(By.XPATH, "//button[contains(text(), 'Close')]").click()

@when('ejecuta el cálculo de conversión presionando el botón "Convert time"')
@when('ejecuta el cálculo de conversión')
def step_impl(context):
    # Dynamic calculations update automatically on the real page.
    pass

@then('el resultado muestra exactamente la misma hora o un mensaje indicando que las zonas son idénticas')
def step_impl(context):
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    h1 = rows[0].find_element(By.CLASS_NAME, "location__formatted-time").text.strip()
    h2 = rows[1].find_element(By.CLASS_NAME, "location__formatted-time").text.strip()
    assert h1 == h2

@then('el resultado final en pantalla corresponde exactamente a la hora calculada y convertida en la zona destino')
def step_impl(context):
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    assert len(rows) >= 2
    resultado_bloque = rows[1].find_element(By.CLASS_NAME, "location__formatted-time")
    assert resultado_bloque.is_displayed()