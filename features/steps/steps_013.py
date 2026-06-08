from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    try:
        context.driver.switch_to.alert.accept()
    except Exception:
        pass

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
    btn = context.driver.find_element(By.CSS_SELECTOR, ".ladda-button")
    context.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", btn)

@then('se muestra una pantalla o mensaje de confirmación de recepción del mensaje')
def step_impl(context):
    # Acepta redirección a feedback-save.php O texto de confirmación en página
    WebDriverWait(context.driver, 15).until(
        lambda d: "feedback-save" in d.current_url
                  or "thank you" in d.find_element(By.TAG_NAME, "body").text.lower()
                  or "sent" in d.find_element(By.TAG_NAME, "body").text.lower()
                  or "received" in d.find_element(By.TAG_NAME, "body").text.lower()
                  or "feedback" in d.current_url and d.find_elements(By.CSS_SELECTOR, ".alert.success")
    )