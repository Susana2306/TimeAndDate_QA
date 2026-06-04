from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario abre la página principal de timeanddate.com')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com")

@when('hace clic en el enlace de "Sign In" en el header')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Sign In')]"))
    ).click()

@when('ingresa un correo y contraseña válidos')
def step_impl(context):
    context.driver.find_element(By.ID, "email").send_keys("test_user_kevin")
    context.driver.find_element(By.ID, "password").send_keys("Pass123*")

@when('presiona el botón de iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@type='submit']").click()

@when('navega a la sección de configuración "My Units" (/custom/)')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/custom/")

@when('cambia la ciudad base a "Bogotá" y el idioma de la interfaz')
def step_impl(context):
    box = context.driver.find_element(By.ID, "homecity")
    box.clear()
    box.send_keys("Bogota")

@when('guarda los cambios de personalización')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save settings')]").click()

@then('el perfil se actualiza correctamente y las preferencias se guardan en la interfaz')
def step_impl(context):
    msg = context.driver.find_element(By.CLASS_NAME, "alert-success")
    assert msg.is_displayed()

@given('que el usuario está en la pantalla de inicio de sesión ("Sign In")')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/custom/login.html")

@when('ingresa un usuario no registrado o una contraseña incorrecta')
def step_impl(context):
    context.driver.find_element(By.ID, "email").send_keys("invalido@gmail.com")
    context.driver.find_element(By.ID, "password").send_keys("falsa123")

@when('intenta acceder al sistema')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@type='submit']").click()


@then('el sistema deniega el acceso y muestra un mensaje de error en el formulario')
def step_impl(context):
    error = context.driver.find_element(By.CLASS_NAME, "err").text
    assert "incorrect" in error.lower() or "failed" in error.lower()

@given('que el usuario se encuentra autenticado en su perfil')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/custom/")

@when('va a la configuración de "My Units" e intenta buscar una ciudad inválida como "{ciudad}"')
def step_impl(context, ciudad):
    box = context.driver.find_element(By.ID, "homecity")
    box.clear()
    box.send_keys(ciudad)

@when('guarda las modificaciones')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//button[contains(text(),'Save settings')]").click()

@then('la ciudad inválida no se guarda y el reloj y clima mantienen la configuración anterior')
def step_impl(context):
    # Verifica que aparezca un mensaje de alerta nativo de error
    alerta_error = context.driver.find_element(By.CLASS_NAME, "err")
    assert alerta_error.is_displayed()

@given('que el usuario modificó exitosamente su ciudad base a "Bogotá" en sus preferencias')
def step_impl(context):
    pass  # Precondición lógica basada en cookies o estado previo

@when('navega por los diferentes módulos de la plataforma de timeanddate')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/worldclock/")

@then('la ciudad configurada en preferencias se refleja automáticamente en las consultas de reloj mundial y clima')
def step_impl(context):
    header_city = context.driver.find_element(By.ID, "nav-bc").text
    assert "Bogota" in header_city or "Colombia" in header_city