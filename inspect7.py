from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("=== TIMER - Edit form fields ===")
driver.get("https://www.timeanddate.com/timer/")
time.sleep(3)
edit_btn = driver.find_element(By.CSS_SELECTOR, ".c-timer__edit")
edit_btn.click()
time.sleep(2)
print("  After clicking Edit - inputs:")
for el in driver.find_elements(By.TAG_NAME, "input"):
    print(f"    id={el.get_attribute('id')!r} name={el.get_attribute('name')!r} class={el.get_attribute('class')!r} value={el.get_attribute('value')!r} displayed={el.is_displayed()}")
print("  After clicking Edit - buttons:")
for el in driver.find_elements(By.TAG_NAME, "button"):
    if el.is_displayed():
        print(f"    class={el.get_attribute('class')!r} text={el.text!r}")
# Check forms
for form in driver.find_elements(By.TAG_NAME, "form"):
    print(f"  form: id={form.get_attribute('id')!r} class={form.get_attribute('class')!r}")

driver.quit()
print("\nDONE")
