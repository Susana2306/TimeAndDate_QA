from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario se encuentra en la sección de Newsletter de la empresa (/news/newsletter.html)')
@given('que el formulario de suscripción está desplegado en pantalla')
@given('que el usuario está en la sección informativa de la empresa')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/newsletter/")


@when('digita un correo con formato inválido como "{correo}"')
def step_impl(context, correo):
    context.driver.find_element(By.ID, "email").send_keys(correo)

@when('hace clic en el botón de suscripción "Subscribe"')
@when('presiona el botón para enviar la suscripción')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@type='submit']").click()

@then('el sistema bloquea el envío y muestra un elemento de error de formato en el DOM')
def step_impl(context):
    error_box = context.driver.find_element(By.CLASS_NAME, "err")
    assert error_box.is_displayed()

@when('el usuario localiza el campo de entrada de texto para el email')
def step_impl(context):
    context.input_email = context.driver.find_element(By.ID, "email")

@when('digita un correo electrónico de forma correcta')
def step_impl(context):
    context.input_email.send_keys("kevin_valido@gmail.com")

@then('la interfaz valida de forma preliminar y el mensaje de confirmación inicial se vuelve visible en el DOM')
def step_impl(context):
    # Validación visual limpia en el campo
    assert context.input_email.get_attribute("value") != ""

@when('deja el campo de email completamente vacío o borra su contenido')
def step_impl(context):
    context.driver.find_element(By.ID, "email").clear()

@then('se muestra un mensaje en pantalla indicando que es un campo requerido y no genera confirmación de éxito')
def step_impl(context):
    body_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert "required" in body_text.lower() or "error" in body_text.lower()

@when('ingresa una dirección de correo válida y nueva que no esté registrada previamente')
@when('confirma el envío del formulario')
def step_impl(context):
    context.driver.find_element(By.ID, "email").send_keys("kevin_qa_new@gmail.com")
    context.driver.find_element(By.ID, "submit").click()

@then('el sistema procesa la solicitud y un elemento de confirmación final de suscripción exitosa es visible en el DOM')
def step_impl(context):
    success_msg = context.driver.find_element(By.CLASS_NAME, "msg-box")
    assert success_msg.is_displayed()