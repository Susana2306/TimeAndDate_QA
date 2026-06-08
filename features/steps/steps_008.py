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
        (By.XPATH, "//table[contains(@class,'tb-theme')]//td[a[contains(text(),'Bogot')]]/following-sibling::td[@class='rbi'][1]")
    ))
    context.hora_inicial = fila.text.strip()

@when('espera unos segundos')
def step_impl(context):
    time.sleep(3)

@then('la hora mostrada en el reloj se ha actualizado con respecto a la lectura anterior')
def step_impl(context):
    XPATH = "//table[contains(@class,'tb-theme')]//td[a[contains(text(),'Bogot')]]/following-sibling::td[@class='rbi'][1]"
    WebDriverWait(context.driver, 70).until(
        lambda d: d.find_element(By.XPATH, XPATH).text.strip() != context.hora_inicial
    )
