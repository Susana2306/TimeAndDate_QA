from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario se encuentra en la página de clima de "Bogotá"')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/weather/colombia/bogota")

@when('verifica las condiciones actuales de temperatura')
def step_impl(context):
    current_temp = context.driver.find_element(By.ID, "qlook").text
    assert len(current_temp) > 0

@when('navega mediante el menú a la pestaña de "Sun & Moon" (Sol y Luna)')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, "Sun & Moon").click()


@then('se visualizan las horas de salida y puesta del sol junto con la fase lunar actual de Bogotá')
def step_impl(context):
    WebDriverWait(context.driver, 15).until(
        lambda d: "Sunrise" in d.find_element(By.TAG_NAME, "body").text
                  or "Moon" in d.find_element(By.TAG_NAME, "body").text
    )