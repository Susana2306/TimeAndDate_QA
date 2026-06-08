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
options.add_argument("--start-maximized")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_window_size(1920, 1080)

# 1. Main page - what does site-nav-login do?
print("=== MAIN PAGE - site-nav-login ===")
driver.get("https://www.timeanddate.com")
time.sleep(3)
btn = driver.find_element(By.ID, "site-nav-login")
print(f"  button: id={btn.get_attribute('id')!r} class={btn.get_attribute('class')!r} displayed={btn.is_displayed()} enabled={btn.is_enabled()}")
print(f"  button tag={btn.tag_name} type={btn.get_attribute('type')!r}")
# What form does it belong to?
try:
    form = btn.find_element(By.XPATH, "./ancestor::form")
    print(f"  parent form: id={form.get_attribute('id')!r} action={form.get_attribute('action')!r}")
except:
    print("  no parent form")
# What's the parent element?
parent = btn.find_element(By.XPATH, "..")
print(f"  parent: tag={parent.tag_name} class={parent.get_attribute('class')!r} id={parent.get_attribute('id')!r}")

# Click and see what happens
btn.click()
time.sleep(2)
print(f"  URL after click: {driver.current_url}")
print(f"  Page title after click: {driver.title}")
# Check if login form appeared
for sel in ["#email", "input[type='email']", "input[type='password']", ".login-form", "#login"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  login element found: {sel!r} displayed={el.is_displayed()}")
    except:
        pass

# 2. Countdown create - home/logo link
print("\n=== COUNTDOWN/CREATE - home link ===")
driver.get("https://www.timeanddate.com/countdown/create")
time.sleep(3)
# Find all anchors whose href is the home page
for a in driver.find_elements(By.TAG_NAME, "a"):
    href = a.get_attribute("href") or ""
    if href.rstrip("/") == "https://www.timeanddate.com" or href == "https://www.timeanddate.com/":
        print(f"  home link: href={href!r} class={a.get_attribute('class')!r} id={a.get_attribute('id')!r} text={a.text!r}")
# Also check the logo
for sel in [".logo", "#logo", "[class*='logo']", "header a", ".site-nav-bar a"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  {sel!r}: href={el.get_attribute('href')!r} class={el.get_attribute('class')!r}")
    except:
        pass

# 3. /custom/ page without login - what happens?
print("\n=== /custom/ PAGE (no login) ===")
driver.get("https://www.timeanddate.com/custom/")
time.sleep(3)
print(f"  URL after navigate: {driver.current_url}")
for el in driver.find_elements(By.TAG_NAME, "input")[:10]:
    print(f"  input: id={el.get_attribute('id')!r} name={el.get_attribute('name')!r} type={el.get_attribute('type')!r}")

# 4. Weather page - search then check temperature class on result page
print("\n=== WEATHER - search Medellin result ===")
driver.get("https://www.timeanddate.com/weather/")
time.sleep(3)
inp = driver.find_element(By.CSS_SELECTOR, ".picker-city__input")
inp.send_keys("Medellin")
time.sleep(2)
# Check autocomplete
for sel in [".autocomplete li", ".picker-city__suggestion", "[class*='suggest']", ".asu li"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  weather autocomplete {sel!r}: count={len(els)} first={els[0].text!r}")
# Try clicking search button
driver.find_element(By.CSS_SELECTOR, ".picker-city__button").click()
time.sleep(3)
print(f"  URL after search: {driver.current_url}")
# Check temperature element
for sel in [".h2", "#qlook", ".h1", ".bk-focus__qlook", "[class*='temp']"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  {sel!r}: text={el.text[:60]!r}")
    except:
        pass

# 5. Worldclock - city search then check "ct" id
print("\n=== WORLDCLOCK - search Tokio result ===")
driver.get("https://www.timeanddate.com/worldclock/")
time.sleep(3)
inp = driver.find_element(By.CSS_SELECTOR, ".picker-city__input")
inp.send_keys("Tokio")
time.sleep(2)
# Check autocomplete options
for sel in [".autocomplete li", ".picker-city__suggestion", ".asu li", "[class*='suggest'] li"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  worldclock autocomplete {sel!r}: count={len(els)} first={els[0].text!r}")
btn = driver.find_element(By.CSS_SELECTOR, ".picker-city__button")
btn.click()
time.sleep(3)
print(f"  URL after Tokio search: {driver.current_url}")
for sel in ["#ct", ".h1", "#clock"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  {sel!r}: text={el.text[:60]!r}")
    except:
        pass

# 6. Converter - check location__formatted-time and location__row
print("\n=== CONVERTER - after adding Bogota ===")
driver.get("https://www.timeanddate.com/worldclock/converter.html")
time.sleep(3)
inp = driver.find_element(By.ID, "addtxt")
inp.send_keys("Bogota")
time.sleep(3)
# Click first autocomplete result
for sel in [".asu li a", ".citypicker__suggestions li a", "[class*='suggest'] li a"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  autocomplete {sel!r}: first={els[0].text!r}")
        els[0].click()
        time.sleep(2)
        break
# Check location rows
for sel in [".location__row", ".location__formatted-time", "[class*='location']"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  {sel!r}: count={len(els)} first_text={els[0].text[:60]!r}")

driver.quit()
print("\nDONE")
