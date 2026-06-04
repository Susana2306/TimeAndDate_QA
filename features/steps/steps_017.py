from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario ingresa la sección principal del clima')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/weather/")

@when('busca cualquier ciudad válida')
def step_impl(context):
    search = context.driver.find_element(By.CLASS_NAME, "picker-city__input")
    search.send_keys("Medellin")
    context.driver.find_element(By.CLASS_NAME, "picker-city__button").click()


@then('el panel de resultados muestra un valor numérico acompañado del símbolo "°C" o "°F"')
def step_impl(context):
    temp_txt = context.driver.find_element(By.CLASS_NAME, "h2").text
    assert "°" in temp_txt