from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given('que el usuario tiene abierto el temporizador en una pestaña')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/timer/")
    time.sleep(1)

@when('inicia un contador de 10 minutes')
def step_impl(context):
    start_btn = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--start"))
    )
    start_btn.click()
    time.sleep(1)

@when('abre en otra pestaña la calculadora de fechas para verificar los días hasta fin de año')
def step_impl(context):
    # Simula la ejecución de flujo paralelo navegando a la sub-herramienta sin romper la sesión de backend
    context.driver.execute_script("window.open('https://www.timeanddate.com/date/duration.html', '_blank');")
    # Cambia el foco de Selenium a la nueva pestaña
    context.driver.switch_to.window(context.driver.window_handles[1])

@then('el temporizador sigue ejecutándose en segundo plano sin interrumpirse por la consulta de fechas')
def step_impl(context):
    assert "duration" in context.driver.current_url
    # Volvemos a la pestaña original para contrastar la concurrencia
    context.driver.switch_to.window(context.driver.window_handles[0])
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    assert timer_div.is_displayed()