from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario ingresa al creador de cuenta regresiva para un evento')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/countdown/create")

@when('llena el título del evento con "Reunión GITESI"')
def step_impl(context):
    context.driver.find_element(By.ID, "msg").send_keys("Reunión GITESI")

@when('presiona el botón o enlace para cancelar o regresar al inicio')
def step_impl(context):
    # Clic al enlace/logo de Home para simular la cancelación deliberada del flujo
    context.driver.find_element(By.XPATH, "//a[@href='https://www.timeanddate.com/']").click()


@then('el sistema regresa a la página anterior sin generar ni guardar la cuenta regresiva')
def step_impl(context):
    assert "countdown/create" not in context.driver.current_url