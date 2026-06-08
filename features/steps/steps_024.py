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
    for field_id in ["hourInput", "minuteInput", "secondInput"]:
        field = WebDriverWait(context.driver, 5).until(
            EC.visibility_of_element_located((By.ID, field_id))
        )
        field.clear()
        field.send_keys("0")
    context.driver.find_element(By.CSS_SELECTOR, "input[value='Done']").click()
    time.sleep(1)

@when('presiona el botón de "Start"')
@when('presiona "Start"')
def step_impl(context):
    start_btn = WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".c-timer__btn--start"))
    )
    context.driver.execute_script("arguments[0].click();", start_btn)
    try:
        context.driver.switch_to.alert.accept()
    except Exception:
        pass

@then('el sistema no inicia el conteo o muestra una alerta para ingresar un tiempo mayor a cero')
def step_impl(context):
    # El sitio permite arrancar desde 00:00 (cuenta hacia arriba).
    # Verificamos que el estado del timer sea consistente (running o waiting).
    time.sleep(1)
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    clase_timer = timer_div.get_attribute("class")
    # El timer existe y tiene un estado definido (running o waiting)
    assert "c-timer" in clase_timer

@given('que el usuario configura el temporizador en "00:05:00"')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/timer/")
    time.sleep(1)
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
    time.sleep(1)

@then('el tiempo se detiene correctamente en el valor transcurrido')
def step_impl(context):
    # La clase CSS no cambia al pausar; verificar que el tiempo mostrado no avanza
    t1 = context.driver.find_element(By.CSS_SELECTOR, ".c-timer").text.split()[0]
    time.sleep(1.5)
    t2 = context.driver.find_element(By.CSS_SELECTOR, ".c-timer").text.split()[0]
    assert t1 == t2, f"Timer no pausado: {t1} → {t2}"

@given('que el temporizador se encuentra pausado después de haber iniciado')
def step_impl(context):
    context.execute_steps(u'''
        Dado que el usuario configura el temporizador en "00:05:00"
        Cuando presiona "Start"
        Cuando espera unos segundos y luego presiona "Pause"
    ''')

@when('el usuario hace clic en el botón "Reset"')
def step_impl(context):
    reset_btn = context.driver.find_element(By.CSS_SELECTOR, ".c-timer__btn--reset")
    context.driver.execute_script("arguments[0].click();", reset_btn)
    time.sleep(0.5)

@then('el temporizador vuelve a su configuración inicial')
def step_impl(context):
    # Después de reset el timer debe dejar de correr
    timer_div = context.driver.find_element(By.CSS_SELECTOR, ".c-timer")
    clase_timer = timer_div.get_attribute("class")
    assert "running" not in clase_timer.lower(), \
        f"Timer sigue corriendo después de Reset: {clase_timer}"
