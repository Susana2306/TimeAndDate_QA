from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario ingresa a la sección principal del clima')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/weather/")

@when('busca cualquier ciudad válida')
def step_impl(context):
    search = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.picker-city__input"))
    )
    context.driver.execute_script("arguments[0].click();", search)
    search.send_keys("Medellin")
    item = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='asu']/li/a"))
    )
    context.driver.execute_script("arguments[0].click();", item)


@then('el panel de resultados muestra un valor numérico acompañado del símbolo "°C" o "°F"')
def step_impl(context):
    temp_el = WebDriverWait(context.driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "h2"))
    )
    assert "°" in temp_el.text