from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, json

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

pages = {
    "main": "https://www.timeanddate.com",
    "login": "https://www.timeanddate.com/custom/login.html",
    "newsletter": "https://www.timeanddate.com/newsletter/",
    "feedback": "https://www.timeanddate.com/information/feedback.html",
    "countdown": "https://www.timeanddate.com/countdown/create",
    "weather_bogota": "https://www.timeanddate.com/weather/colombia/bogota",
    "duration": "https://www.timeanddate.com/date/duration.html",
    "worldclock": "https://www.timeanddate.com/worldclock/",
    "converter": "https://www.timeanddate.com/worldclock/converter.html",
    "timer": "https://www.timeanddate.com/timer/",
}

for name, url in pages.items():
    driver.get(url)
    time.sleep(3)
    inputs = driver.find_elements(By.TAG_NAME, "input")
    textareas = driver.find_elements(By.TAG_NAME, "textarea")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    selects = driver.find_elements(By.TAG_NAME, "select")

    print(f"\n{'='*60}")
    print(f"PAGE: {name}  URL: {url}")
    print("INPUTS:")
    for e in inputs[:25]:
        print(f"  id={e.get_attribute('id')!r} name={e.get_attribute('name')!r} type={e.get_attribute('type')!r} class={e.get_attribute('class')!r} placeholder={e.get_attribute('placeholder')!r}")
    print("TEXTAREAS:")
    for e in textareas[:10]:
        print(f"  id={e.get_attribute('id')!r} name={e.get_attribute('name')!r} class={e.get_attribute('class')!r}")
    print("BUTTONS:")
    for e in buttons[:20]:
        print(f"  id={e.get_attribute('id')!r} class={e.get_attribute('class')!r} type={e.get_attribute('type')!r} text={e.text[:60]!r}")
    print("SELECTS:")
    for e in selects[:10]:
        print(f"  id={e.get_attribute('id')!r} name={e.get_attribute('name')!r} class={e.get_attribute('class')!r}")

    # Extra: sign-in link on main page
    if name == "main":
        print("HEADER LINKS:")
        for a in driver.find_elements(By.CSS_SELECTOR, "header a, #nav a, .nav a, nav a")[:30]:
            print(f"  text={a.text!r} href={a.get_attribute('href')!r} id={a.get_attribute('id')!r} class={a.get_attribute('class')!r}")

driver.quit()
print("\nDONE")
