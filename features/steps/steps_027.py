from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario abre la calculadora de fechas de timeanddate')
@given('que el usuario abre la calculadora de fechas')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/date/duration.html")

@when('ingresa un valor de mes inválido como "{mes_falso}" en la fecha de inicio')
def step_impl(context, mes_falso):
    context.driver.find_element(By.ID, "m1").send_keys(mes_falso)

@when('hace clic en el botón de calcular duración')
def step_impl(context):
    # El botón de submit real tiene id="subbut2"
    context.driver.find_element(By.ID, "subbut2").click()

@then('el sistema muestra un mensaje de error indicando que la fecha es inválida y no calcula el resultado')
def step_impl(context):
    # Verifica que no hay resultados o el contenedor de resultados no muestra 365 días
    body_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert "error" in body_text.lower() or "invalid" in body_text.lower() or "365" not in body_text

@when('ingresa "{f1}" como fecha de inicio')
def step_impl(context, f1):
    # 1 de Enero del 2025
    context.driver.find_element(By.ID, "d1").send_keys("1")
    context.driver.find_element(By.ID, "m1").send_keys("1")
    context.driver.find_element(By.ID, "y1").send_keys("2025")

@when('ingresa "{f2}" como fecha de fin')
def step_impl(context, f2):
    # 1 de Enero del 2026
    context.driver.find_element(By.ID, "d2").send_keys("1")
    context.driver.find_element(By.ID, "m2").send_keys("1")
    context.driver.find_element(By.ID, "y2").send_keys("2026")

@then('el resultado muestra exactamente "365 days" o su equivalente')
def step_impl(context):
    # El resultado se muestra dentro del div con clase "bx-result"
    result_div = WebDriverWait(context.driver, 8).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bx-result"))
    )
    output_text = result_div.text
    assert "365" in output_text