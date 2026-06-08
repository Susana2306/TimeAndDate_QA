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

# 1. TIMER - pause button class when running
print("=== TIMER - pause button ===")
driver.get("https://www.timeanddate.com/timer/")
time.sleep(3)
# Initial state buttons
print("  Initial buttons:")
for btn in driver.find_elements(By.CSS_SELECTOR, "[class*='c-timer__btn']"):
    print(f"    class={btn.get_attribute('class')!r} displayed={btn.is_displayed()} text={btn.text!r}")

# Check reset button state initially
for sel in [".c-timer__btn--reset"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    for el in els:
        print(f"  {sel!r}: displayed={el.is_displayed()} enabled={el.is_enabled()} class={el.get_attribute('class')!r}")

# Click start
start = driver.find_element(By.CSS_SELECTOR, ".c-timer__btn--start")
start.click()
time.sleep(2)
print("  After START buttons:")
for btn in driver.find_elements(By.CSS_SELECTOR, "[class*='c-timer__btn']"):
    print(f"    class={btn.get_attribute('class')!r} displayed={btn.is_displayed()} text={btn.text!r}")

# Try to find pause
for sel in [".c-timer__btn--pause", "[class*='pause']", "button[class*='pause']"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  pause {sel!r}: count={len(els)} class={els[0].get_attribute('class')!r} displayed={els[0].is_displayed()}")
    else:
        print(f"  pause {sel!r}: NOT FOUND")

# Check timer container class
timer = driver.find_element(By.CSS_SELECTOR, ".c-timer")
print(f"  .c-timer class while running: {timer.get_attribute('class')!r}")

# 2. NEWSLETTER - submit valid email and check success
print("\n=== NEWSLETTER - valid email submit ===")
driver.get("https://www.timeanddate.com/newsletter/")
time.sleep(3)
driver.find_element(By.ID, "email").send_keys("totally_new_test_xyz_9999@gmail.com")
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
time.sleep(4)
print(f"  URL after submit: {driver.current_url!r}")
# Check for success elements
for sel in [".msg-box", ".msg", ".ok", ".success", ".alert.ok", ".alert.success", ".conf", "#conf", ".message", ".thanks"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  FOUND {sel!r}: text={el.text[:80]!r} displayed={el.is_displayed()}")
    except:
        pass
# Body text check
body = driver.find_element(By.TAG_NAME, "body").text
print(f"  body contains 'thank': {'thank' in body.lower()}")
print(f"  body contains 'success': {'success' in body.lower()}")
print(f"  body contains 'confirm': {'confirm' in body.lower()}")
# Find any element containing success-like text
for el in driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, div.msg, div.ok, div.conf, span.ok"):
    txt = el.text.strip()
    if txt and any(w in txt.lower() for w in ["thank", "subscri", "confirm", "success", "sent"]):
        print(f"  success-like: tag={el.tag_name} class={el.get_attribute('class')!r} text={txt[:100]!r}")

# 3. NEWSLETTER - empty email native validation
print("\n=== NEWSLETTER - empty email validation ===")
driver.get("https://www.timeanddate.com/newsletter/")
time.sleep(3)
email_field = driver.find_element(By.ID, "email")
# Try clicking submit without filling email
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
time.sleep(2)
print(f"  validation message: {email_field.get_attribute('validationMessage')!r}")
print(f"  validity.valueMissing: {driver.execute_script('return arguments[0].validity.valueMissing', email_field)}")
# Look for any visible error
for sel in [".err", ".error", ".alert", ".alert.error", "p.err"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  {sel!r}: text={el.text!r} displayed={el.is_displayed()}")
    except:
        pass
body_text = driver.find_element(By.TAG_NAME, "body").text
print(f"  body has 'required': {'required' in body_text.lower()}")
print(f"  body has 'error': {'error' in body_text.lower()}")

driver.quit()
print("\nDONE")
