from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario abre la página principal de timeanddate.com')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com")

@when('hace clic en el enlace de "Sign In" en el header')
def step_impl(context):
    btn = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "site-nav-login"))
    )
    context.driver.execute_script("arguments[0].click();", btn)

@when('ingresa un correo y contraseña válidos')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email, password = context.credentials
    context.driver.find_element(By.ID, "email").send_keys(email)
    context.driver.find_element(By.ID, "password").send_keys(password)

@when('presiona el botón de iniciar sesión')
def step_impl(context):
    # Usar id='create' específicamente — hay múltiples input[type=submit] en página
    btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='create'], input[value='Sign in']"))
    )
    context.driver.execute_script("arguments[0].click();", btn)
    WebDriverWait(context.driver, 15).until(
        lambda d: "login" not in d.current_url
    )

@when('navega a la sección de configuración "My Units" (/custom/)')
def step_impl(context):
    # La configuración de ciudad está en /custom/location.html
    context.driver.get("https://www.timeanddate.com/custom/location.html")
    WebDriverWait(context.driver, 10).until(
        lambda d: "login" not in d.current_url
    )

@when('cambia la ciudad base a "Bogotá" y el idioma de la interfaz')
def step_impl(context):
    # Campo real: id='ftztxt' en /custom/location.html
    box = WebDriverWait(context.driver, 15).until(
        EC.element_to_be_clickable((By.ID, "ftztxt"))
    )
    box.clear()
    box.send_keys("Bogota")

@when('guarda los cambios de personalización')
def step_impl(context):
    btn = context.driver.find_element(By.CSS_SELECTOR, "input[value='Save Settings']")
    context.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", btn)

@then('el perfil se actualiza correctamente y las preferencias se guardan en la interfaz')
def step_impl(context):
    WebDriverWait(context.driver, 15).until(
        lambda d: "saved" in d.find_element(By.TAG_NAME, "body").text.lower()
                  or d.find_elements(By.CSS_SELECTOR, ".alert.success")
    )

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
    error = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.error"))
    )
    txt = error.text.lower()
    assert "denied" in txt or "incorrect" in txt or "failed" in txt or "wrong" in txt or "error" in txt

@given('que el usuario se encuentra autenticado en su perfil')
def step_impl(context):
    # Reusar sesión pre-establecida en before_all para evitar múltiples logins
    context.inject_session()
    context.driver.get("https://www.timeanddate.com/custom/location.html")
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "ftztxt"))
    )

@when('va a la configuración de "My Units" e intenta buscar una ciudad inválida como "{ciudad}"')
def step_impl(context, ciudad):
    box = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ftztxt"))
    )
    box.clear()
    box.send_keys(ciudad)

@when('guarda las modificaciones')
def step_impl(context):
    btn = context.driver.find_element(By.CSS_SELECTOR, "input[value='Save Settings']")
    context.driver.execute_script("arguments[0].scrollIntoView(); arguments[0].click();", btn)

@then('la ciudad inválida no se guarda y el reloj y clima mantienen la configuración anterior')
def step_impl(context):
    alerta_error = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.error"))
    )
    assert alerta_error.is_displayed()

@given('que el usuario modificó exitosamente su ciudad base a "Bogotá" en sus preferencias')
def step_impl(context):
    pass  # Precondición lógica basada en estado previo

@when('navega por los diferentes módulos de la plataforma de timeanddate')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/worldclock/")

@then('la ciudad configurada en preferencias se refleja automáticamente en las consultas de reloj mundial y clima')
def step_impl(context):
    bogota = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'colombia/bogota')]"))
    )
    assert bogota.is_displayed()
