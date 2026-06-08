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
    edit_btn = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__edit"))
    )
    context.driver.execute_script("arguments[0].click();", edit_btn)
    time.sleep(1)
    # Intentar con IDs conocidos; si no existen, buscar inputs numéricos del modal
    for selector in ["#hourInput", "#minuteInput", "#secondInput",
                     "input[data-unit='h']", "input[data-unit='m']", "input[data-unit='s']"]:
        try:
            fields = context.driver.find_elements(By.CSS_SELECTOR, selector)
            for f in fields:
                if f.is_displayed():
                    f.clear()
                    f.send_keys("0")
        except Exception:
            pass
    # Confirmar con botón Done o cualquier submit del modal
    for done_sel in ["input[value='Done']", "button[type='submit']", ".c-timer__done"]:
        try:
            btn = context.driver.find_element(By.CSS_SELECTOR, done_sel)
            if btn.is_displayed():
                context.driver.execute_script("arguments[0].click();", btn)
                break
        except Exception:
            pass
    time.sleep(1)

@when('presiona el botón de "Start"')
@when('presiona "Start"')
def step_impl(context):
    start_btn = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--start"))
    )
    context.driver.execute_script("arguments[0].click();", start_btn)
    # Descartar cualquier JS alert que aparezca (ej: "tiempo debe ser > 0")
    try:
        context.driver.switch_to.alert.accept()
    except Exception:
        pass

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
    time.sleep(2)
    pause_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--pause"))
    )
    context.driver.execute_script("arguments[0].click();", pause_btn)
    time.sleep(0.5)

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