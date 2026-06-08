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

# 1. Main page - nav Sign In link (actual href, not hidden button)
print("=== MAIN PAGE - all sign-in related links ===")
driver.get("https://www.timeanddate.com")
time.sleep(3)
for a in driver.find_elements(By.TAG_NAME, "a"):
    href = a.get_attribute("href") or ""
    if "login" in href or "signin" in href or "sign-in" in href:
        print(f"  login link: href={href!r} text={a.text!r} class={a.get_attribute('class')!r} id={a.get_attribute('id')!r} displayed={a.is_displayed()}")
# Check computed visibility of site-nav-login
btn = driver.find_element(By.ID, "site-nav-login")
style = driver.execute_script("return window.getComputedStyle(arguments[0]).display", btn)
visibility = driver.execute_script("return window.getComputedStyle(arguments[0]).visibility", btn)
print(f"  site-nav-login computed: display={style!r} visibility={visibility!r}")
# Check ALL nav-bar elements
for el in driver.find_elements(By.CSS_SELECTOR, ".site-nav-bar *")[:20]:
    if el.get_attribute("id") or "login" in (el.get_attribute("class") or ""):
        print(f"  nav-bar el: tag={el.tag_name} id={el.get_attribute('id')!r} class={el.get_attribute('class')!r} displayed={el.is_displayed()} href={el.get_attribute('href')!r}")

# 2. Countdown/create - ALL anchor links
print("\n=== COUNTDOWN/CREATE - all links with href ===")
driver.get("https://www.timeanddate.com/countdown/create")
time.sleep(3)
for a in driver.find_elements(By.TAG_NAME, "a"):
    href = a.get_attribute("href") or ""
    if "timeanddate.com" in href and href.rstrip("/").endswith("timeanddate.com"):
        print(f"  home-href: {href!r} class={a.get_attribute('class')!r} id={a.get_attribute('id')!r}")
# Logo/site-name link
for sel in ["[class*='logo']", "[class*='brand']", "[class*='home']", "header a:first-child", ".site-nav-bar__logo", "a.site-nav-bar"]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  {sel!r}: href={el.get_attribute('href')!r} class={el.get_attribute('class')!r}")
    except:
        pass
# First link in nav area
for a in driver.find_elements(By.CSS_SELECTOR, "header a, .site-nav-bar a, nav a")[:5]:
    print(f"  first nav links: href={a.get_attribute('href')!r} class={a.get_attribute('class')!r} text={a.text[:30]!r}")

# 3. /custom/ page - what's the actual URL it redirects to?
print("\n=== /custom/ redirect ===")
driver.get("https://www.timeanddate.com/custom/")
time.sleep(3)
print(f"  final URL: {driver.current_url!r}")
for el in driver.find_elements(By.TAG_NAME, "input")[:5]:
    print(f"  input: id={el.get_attribute('id')!r} name={el.get_attribute('name')!r}")

# 4. Weather - check what picker-city__button does
print("\n=== WEATHER - after search Medellin ===")
driver.get("https://www.timeanddate.com/weather/")
time.sleep(3)
inp = driver.find_element(By.CSS_SELECTOR, ".picker-city__input")
inp.send_keys("Medellin")
time.sleep(3)
# Check autocomplete appeared
for sel in [".asu", ".asu li", "[class*='autoc']", "[class*='picker-city__']"]:
    els = driver.find_elements(By.CSS_SELECTOR, sel)
    if els:
        print(f"  autocomplete {sel!r}: count={len(els)}")
        for el in els[:3]:
            print(f"    text={el.text!r} href={el.get_attribute('href')!r}")
# Click button
driver.find_element(By.CSS_SELECTOR, ".picker-city__button").click()
time.sleep(4)
print(f"  URL after click: {driver.current_url!r}")
try:
    el = driver.find_element(By.CLASS_NAME, "h2")
    print(f"  .h2 text: {el.text!r}")
except Exception as e:
    print(f"  .h2 NOT FOUND: {e}")
    # Try alternatives
    for sel in ["#qlook", ".qlook", ".temp", "[class*='temp']", "h2"]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            print(f"  alt {sel!r}: text={el.text[:60]!r}")
        except:
            pass

# 5. Timer - verify c-timer state on start
print("\n=== TIMER - start and check state ===")
driver.get("https://www.timeanddate.com/timer/")
time.sleep(3)
timer_div = driver.find_element(By.CSS_SELECTOR, ".c-timer")
print(f"  .c-timer initial class: {timer_div.get_attribute('class')!r}")
# Check start button
start = driver.find_element(By.CSS_SELECTOR, ".c-timer__btn--start")
print(f"  start btn: class={start.get_attribute('class')!r} displayed={start.is_displayed()}")
start.click()
time.sleep(1)
timer_div = driver.find_element(By.CSS_SELECTOR, ".c-timer")
print(f"  .c-timer class after start: {timer_div.get_attribute('class')!r}")
# Check if "running" in class
print(f"  'running' in class: {'running' in timer_div.get_attribute('class')}")

# 6. Worldclock Bogota - check row/time structure
print("\n=== WORLDCLOCK - Bogota row structure ===")
driver.get("https://www.timeanddate.com/worldclock/")
time.sleep(3)
# Try XPath for Bogota time
try:
    fila = driver.find_element(By.XPATH, "//table[contains(@class,'tb-theme')]//td[a[contains(text(),'Bogot')]]/following-sibling::td[@class='rbi'][1]")
    print(f"  Bogota time XPath result: {fila.text!r}")
except Exception as e:
    print(f"  XPath FAIL: {e}")
    # Check the actual table structure
    tbl = driver.find_element(By.CSS_SELECTOR, "table.zebra")
    rows = tbl.find_elements(By.TAG_NAME, "tr")
    for row in rows[:5]:
        tds = row.find_elements(By.TAG_NAME, "td")
        if tds:
            print(f"  row: {[(td.get_attribute('class'), td.text[:20]) for td in tds[:4]]}")

driver.quit()
print("\nDONE")
