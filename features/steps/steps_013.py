from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario abre el formulario de contacto o feedback')
@given('que el formulario de feedback está cargado')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/information/feedback.html")

@when('redacta un mensaje en el campo de descripción')
def step_impl(context):
    context.driver.find_element(By.ID, "body").send_keys("Prueba de automatización - GITESI")

@when('recarga la página o navega hacia atrás antes de enviarlo')
def step_impl(context):
    context.driver.refresh()

@then('la contribución se descarta y el formulario vuelve a su estado vacío')
def step_impl(context):
    valor_campo = context.driver.find_element(By.ID, "body").text
    assert valor_campo == ""

@when('el usuario ingresa su nombre, un correo válido y un mensaje de prueba')
def step_impl(context):
    context.driver.find_element(By.ID, "fullname").send_keys("Kevin Alzate")
    context.driver.find_element(By.ID, "email").send_keys("kevin@gmail.com")
    context.driver.find_element(By.ID, "body").send_keys("Reporte de mejora en interfaz")

@when('hace clic en enviar')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//button[@type='submit']").click()

@then('se muestra una pantalla o mensaje de confirmación de recepción del mensaje')
def step_impl(context):
    # Buscamos un texto o contenedor típico de éxito post-envío
    body_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert "thank you" in body_text.lower() or "sent" in body_text.lower()