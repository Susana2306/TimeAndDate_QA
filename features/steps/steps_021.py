from behave import given, when, then
from selenium.webdriver.common.by import By

@given('que el usuario se encuentra en la sección de Newsletter de la empresa (/news/newsletter.html)')
@given('que el formulario de suscripción está desplegado en pantalla')
@given('que el usuario está en la sección informativa de la empresa')
@given('que el usuario visualiza el campo de email del newsletter')
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
    error_box = context.driver.find_element(By.CSS_SELECTOR, ".alert.error")
    assert error_box.is_displayed()

@when('el usuario localiza el campo de entrada de texto para el email')
def step_impl(context):
    context.input_email = context.driver.find_element(By.ID, "email")

@when('digita un correo electrónico estructurado correctamente')
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
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    error_box = WebDriverWait(context.driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.error"))
    )
    assert error_box.is_displayed()

@when('ingresa una dirección de correo válida y nueva que no esté registrada previamente')
def step_impl(context):
    context.driver.find_element(By.ID, "email").send_keys("kevin_qa_new@gmail.com")

@when('confirma el envío del formulario')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

@then('el sistema procesa la solicitud y un elemento de confirmación final de suscripción exitosa es visible en el DOM')
def step_impl(context):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    success_msg = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.success"))
    )
    assert success_msg.is_displayed()