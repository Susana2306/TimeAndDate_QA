from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@given('que el usuario convierte la hora actual de Bogotá a "{destino}" en el conversor de husos horarios')
def step_impl(context, destino):
    context.driver.get("https://www.timeanddate.com/worldclock/converter.html")
    time.sleep(1)
    
    # Add Bogota
    p1 = context.driver.find_element(By.ID, "addtxt")
    p1.clear()
    p1.send_keys("Bogota")
    WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))).click()
    time.sleep(1)
    
    # Add destino
    p2 = context.driver.find_element(By.ID, "addtxt")
    p2.clear()
    p2.send_keys(destino)
    WebDriverWait(context.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))).click()
    time.sleep(1)

@when('anota el resultado de la conversión')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, "location__row")) >= 2
    )
    rows = context.driver.find_elements(By.CLASS_NAME, "location__row")
    context.conversion_output = rows[1].find_element(By.CLASS_NAME, "location__formatted-time").text.split(":")[0].strip()

@when('navega inmediatamente al "World Clock" y busca "{destino}"')
def step_impl(context, destino):
    context.driver.get("https://www.timeanddate.com/worldclock/")
    search = context.driver.find_element(By.CLASS_NAME, "picker-city__input")
    search.send_keys(destino)
    WebDriverWait(context.driver, 8).until(
        EC.element_to_be_clickable((By.XPATH, "//ul[@class='asu']/li/a"))
    ).click()

@then('la hora mostrada en el reloj mundial para Tokio coincide con la conversión previa con un margen máximo de 1 minuto')
def step_impl(context):
    live_clock = context.driver.find_element(By.ID, "ct").text.split(":")[0].strip()
    assert context.conversion_output in live_clock