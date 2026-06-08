from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 1. Worldclock city page - check "ct" id
print("=== WORLDCLOCK TOKYO - check id='ct' ===")
driver.get("https://www.timeanddate.com/worldclock/japan/tokyo")
time.sleep(3)
for sel in ["#ct", "#time", ".time", "#clock", ".clock", "#c", ".c"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  FOUND {sel!r}: text={el.text[:60]!r} class={el.get_attribute('class')!r}")
    except:
        pass
# Find element with time-like text (HH:MM)
import re
for el in driver.find_elements(By.CSS_SELECTOR, "span, div, p"):
    txt = el.text.strip()
    if re.match(r'^\d{1,2}:\d{2}', txt):
        print(f"  time-like: tag={el.tag_name} id={el.get_attribute('id')!r} class={el.get_attribute('class')!r} text={txt[:40]!r}")
        break

# 2. Weather bogota - Sun & Moon link
print("\n=== WEATHER BOGOTA - Sun & Moon nav link ===")
driver.get("https://www.timeanddate.com/weather/colombia/bogota")
time.sleep(3)
for a in driver.find_elements(By.TAG_NAME, "a"):
    txt = a.text.strip()
    if "sun" in txt.lower() or "moon" in txt.lower() or "sol" in txt.lower():
        print(f"  text={txt!r} href={a.get_attribute('href')!r} class={a.get_attribute('class')!r}")

# Sub-nav links
print("  Sub-nav links:")
for a in driver.find_elements(By.CSS_SELECTOR, ".bk-focus__nav a, nav a, .tab a, .subnav a, [class*='nav'] a")[:15]:
    txt = a.text.strip()
    if txt:
        print(f"    text={txt!r} href={a.get_attribute('href')!r}")

# 3. Newsletter success container
print("\n=== NEWSLETTER - success msg selector ===")
driver.get("https://www.timeanddate.com/newsletter/")
time.sleep(2)
# Check what class/id exists for success after subscription
for sel in [".msg-box", ".success", ".ok", ".msg", "#msg", ".alert.ok", ".alert.success", ".confirm"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  FOUND {sel!r}: displayed={el.is_displayed()} text={el.text[:60]!r}")
    except:
        pass

# 4. Timer - check container class
print("\n=== TIMER - container class ===")
driver.get("https://www.timeanddate.com/timer/")
time.sleep(3)
for sel in [".c-timer", "[class*='c-timer']", "#timer", ".timer"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  FOUND {sel!r}: class={el.get_attribute('class')!r}")
    except:
        pass

# 5. Worldclock main page - table structure for Bogota
print("\n=== WORLDCLOCK MAIN - table structure ===")
driver.get("https://www.timeanddate.com/worldclock/")
time.sleep(3)
for tbl in driver.find_elements(By.TAG_NAME, "table"):
    print(f"  table id={tbl.get_attribute('id')!r} class={tbl.get_attribute('class')!r}")
# Check if Bogota row exists
for a in driver.find_elements(By.CSS_SELECTOR, "table td a"):
    if "bogot" in a.text.lower() or "colombia" in a.text.lower():
        tr = a.find_element(By.XPATH, "./ancestor::tr")
        tds = tr.find_elements(By.TAG_NAME, "td")
        print(f"  Bogota row: tds classes = {[td.get_attribute('class') for td in tds]}")
        print(f"  Bogota row: tds text = {[td.text[:30] for td in tds]}")
        break

driver.quit()
print("\nDONE")
