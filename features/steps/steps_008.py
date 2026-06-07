from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given('que el usuario navega al reloj mundial de timeanddate')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/worldclock/")

@when('obtiene la hora actual para "Colombia - Bogotá"')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    fila = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//table[@id='tz-list']//td[contains(@class,'c')]/a[contains(text(),'Bogot')]/ancestor::tr/td[contains(@class,'time')]")
    ))
    context.hora_inicial = fila.text.strip()

@when('espera unos segundos')
def step_impl(context):
    time.sleep(3)

@then('la hora mostrada en el reloj se ha actualizado con respecto a la lectura anterior')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    fila = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//table[@id='tz-list']//td[contains(@class,'c')]/a[contains(text(),'Bogot')]/ancestor::tr/td[contains(@class,'time')]")
    ))
    hora_actual = fila.text.strip()
    assert hora_actual != context.hora_inicial, \
        f"La hora no se actualizó: antes={context.hora_inicial}, después={hora_actual}"
