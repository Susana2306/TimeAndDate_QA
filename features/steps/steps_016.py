from behave import given, when, then
from selenium.webdriver.common.by import By

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
    assert "countdown" in context.driver.current_url
    cronometro = context.driver.find_element(By.CSS_SELECTOR, "[class*='countdown']")
    assert cronometro.is_displayed()