from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('que el usuario está en el creador de cuenta regresiva')
def step_impl(context):
    context.driver.get("https://www.timeanddate.com/countdown/create")

@when('llena los detalles del evento con fecha futura')
def step_impl(context):
    context.driver.find_element(By.ID, "msg").send_keys("Proyecto IUE Final")
    context.driver.find_element(By.ID, "year").clear()
    context.driver.find_element(By.ID, "year").send_keys("2027")

@when('hace clic en "Create Countdown"')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@type='submit']").click()

@then('se genera una URL única que muestra el cronómetro en vivo hacia la fecha del evento')
def step_impl(context):
    WebDriverWait(context.driver, 15).until(
        lambda d: "countdown" in d.current_url and "create" not in d.current_url
    )
    cronometro = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='countdown']"))
    )
    assert cronometro.is_displayed()