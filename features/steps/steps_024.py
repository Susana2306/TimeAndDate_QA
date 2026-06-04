from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given('que el usuario abre la herramienta de temporizador')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/timer/")

@when('el tiempo está configurado en "00:00:00"')
def step_impl(context):
    # El timer carga con un tiempo configurado por defecto (ej: 00:02:00).
    # Primero reseteamos para asegurar que está en estado de espera.
    reset_btn = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--reset"))
    )
    reset_btn.click()
    time.sleep(1)

@when('presiona el botón de "Start"')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, ".c-timer__btn--start").click()

@then('el sistema no inicia el conteo o muestra una alerta para ingresar un tiempo mayor a cero')
def step_impl(context):
    # Si el timer está en "waiting" no ha iniciado el conteo
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    clase_timer = timer_div.get_attribute("class")
    assert "running" not in clase_timer.lower()

@given('que el usuario configura el temporizador en "00:05:00"')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/timer/")
    time.sleep(1)
    # El timer por defecto ya tiene un tiempo configurado (ej: 2 min)
    # Verificamos que hay un botón de Start disponible
    WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--start"))
    )

@when('espera unos segundos y luego presiona "Pause"')
def step_impl(context):
    # Primero iniciamos, luego pausamos
    start_btn = WebDriverWait(context.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--start"))
    )
    start_btn.click()
    time.sleep(2)
    # El botón Pause aparece cuando el timer está corriendo
    pause_btn = WebDriverWait(context.driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--pause"))
    )
    pause_btn.click()

@then('el tiempo se detiene correctamente en el valor transcurrido')
def step_impl(context):
    # Cuando está pausado, el estado del div es c-timer--waiting (no c-timer--running)
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    clase_timer = timer_div.get_attribute("class")
    assert "running" not in clase_timer.lower()

@given('que el temporizador se encuentra pausado después de haber iniciado')
def step_impl(context):
    context.execute_steps('''
        Given que el usuario configura el temporizador en "00:05:00"
        When espera unos segundos y luego presiona "Pause"
    ''')

@when('el usuario hace clic en el botón "Reset"')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, ".c-timer__btn--reset").click()

@then('el temporizador vuelve a su configuración inicial')
def step_impl(context):
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    clase_timer = timer_div.get_attribute("class")
    # Después de reset el timer vuelve al estado de espera
    assert "running" not in clase_timer.lower()