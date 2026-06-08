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

# 1. Weather Bogota - temperature element
print("=== WEATHER BOGOTA - temperature ===")
driver.get("https://www.timeanddate.com/weather/colombia/bogota")
time.sleep(3)
# Try to find temperature container
for sel in ["#qlook", ".qlook", "#wt-ctx", ".h2", "#t2d", ".cur-con-weather-card"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  FOUND {sel!r}: text={el.text[:80]!r} class={el.get_attribute('class')!r}")
    except:
        print(f"  NOT FOUND: {sel!r}")

# Also get all elements with id containing 'temp' or 'weather'
for el in driver.find_elements(By.CSS_SELECTOR, "[id*='temp'], [id*='weather'], [id*='qlook'], [id*='wt'], [id*='cur']")[:10]:
    print(f"  id_match: id={el.get_attribute('id')!r} class={el.get_attribute('class')!r} text={el.text[:80]!r}")

# Get h2 elements
print("  H2 elements:")
for el in driver.find_elements(By.TAG_NAME, "h2")[:5]:
    print(f"    class={el.get_attribute('class')!r} text={el.text[:80]!r}")

# Get degree symbol elements
print("  Elements with degree symbol:")
src = driver.page_source
idx = src.find("°")
if idx > 0:
    print(f"  Context around °: ...{src[max(0,idx-200):idx+200]}...")

# 2. Login page - error elements
print("\n=== LOGIN - try invalid login to see error ===")
driver.get("https://www.timeanddate.com/custom/login.html")
time.sleep(2)
try:
    driver.find_element(By.ID, "email").send_keys("invalid@test.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass123")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(3)
    for sel in [".err", ".error", ".alert", ".msg", "#msg", ".errmsg", ".login-error"]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            print(f"  FOUND {sel!r}: text={el.text!r} displayed={el.is_displayed()}")
        except:
            pass
    # Check body for error text
    body = driver.find_element(By.TAG_NAME, "body").text
    if "incorrect" in body.lower() or "failed" in body.lower() or "invalid" in body.lower() or "wrong" in body.lower():
        print(f"  Error text found in body")
        # Find specific element
        for el in driver.find_elements(By.CSS_SELECTOR, "p, span, div"):
            txt = el.text.strip()
            if txt and ("incorrect" in txt.lower() or "failed" in txt.lower() or "wrong" in txt.lower() or "invalid" in txt.lower()):
                print(f"    tag={el.tag_name} class={el.get_attribute('class')!r} id={el.get_attribute('id')!r} text={txt[:100]!r}")
except Exception as e:
    print(f"  Error: {e}")

# 3. Newsletter - error elements
print("\n=== NEWSLETTER - try invalid email ===")
driver.get("https://www.timeanddate.com/newsletter/")
time.sleep(2)
try:
    driver.find_element(By.ID, "email").send_keys("notanemail")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    time.sleep(3)
    for sel in [".err", ".error", ".alert", ".msg", "#msg", ".errmsg"]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            print(f"  FOUND {sel!r}: text={el.text!r} displayed={el.is_displayed()}")
        except:
            pass
except Exception as e:
    print(f"  Error: {e}")

# 4. Duration result container
print("\n=== DURATION RESULT ===")
driver.get("https://www.timeanddate.com/date/duration.html")
time.sleep(2)
try:
    driver.find_element(By.ID, "d1").send_keys("1")
    driver.find_element(By.ID, "m1").send_keys("1")
    driver.find_element(By.ID, "y1").send_keys("2025")
    driver.find_element(By.ID, "d2").send_keys("1")
    driver.find_element(By.ID, "m2").send_keys("1")
    driver.find_element(By.ID, "y2").send_keys("2026")
    driver.find_element(By.ID, "subbut2").click()
    time.sleep(3)
    for sel in [".bx-result", "#result", ".result", "#res", ".res", "#answer"]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            print(f"  FOUND {sel!r}: text={el.text[:100]!r} displayed={el.is_displayed()}")
        except:
            pass
    # Find 365
    for el in driver.find_elements(By.CSS_SELECTOR, "p, span, div, td"):
        if "365" in el.text:
            print(f"  365 in: tag={el.tag_name} class={el.get_attribute('class')!r} id={el.get_attribute('id')!r} text={el.text[:100]!r}")
            break
except Exception as e:
    print(f"  Error: {e}")

# 5. Converter - autocomplete list
print("\n=== CONVERTER - autocomplete ===")
driver.get("https://www.timeanddate.com/worldclock/converter.html")
time.sleep(2)
try:
    inp = driver.find_element(By.ID, "addtxt")
    inp.send_keys("Bogota")
    time.sleep(3)
    for sel in [".asu li a", ".autocomplete li", ".ui-autocomplete li", "[class*='autocomplete'] li", "[class*='suggest'] li", ".citypicker__suggestions li"]:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            print(f"  Autocomplete {sel!r}: first={els[0].text!r} count={len(els)}")
    # Generic list items after input
    lis = driver.find_elements(By.CSS_SELECTOR, "ul li a")
    for li in lis[:5]:
        if li.text:
            print(f"  li>a: text={li.text!r} class={li.get_attribute('class')!r}")
except Exception as e:
    print(f"  Error: {e}")

# 6. Worldclock - check tz-list and city search
print("\n=== WORLDCLOCK ===")
driver.get("https://www.timeanddate.com/worldclock/")
time.sleep(2)
try:
    tbl = driver.find_element(By.ID, "tz-list")
    print(f"  tz-list found: {tbl.tag_name}")
except:
    print("  tz-list NOT FOUND")
    # Find tables
    for tbl in driver.find_elements(By.TAG_NAME, "table")[:3]:
        print(f"  table: id={tbl.get_attribute('id')!r} class={tbl.get_attribute('class')!r}")

driver.quit()
print("\nDONE")
