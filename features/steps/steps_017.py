from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario ingresa a la sección principal del clima')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/weather/")

@when('busca cualquier ciudad válida')
def step_impl(context):
    search = context.driver.find_element(By.CLASS_NAME, "picker-city__input")
    search.send_keys("Medellin")
    WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))
    ).click()


@then('el panel de resultados muestra un valor numérico acompañado del símbolo "°C" o "°F"')
def step_impl(context):
    temp_el = WebDriverWait(context.driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "h2"))
    )
    assert "°" in temp_el.text