from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Postavi tačnu lokalnu putanju do chromedriver.exe
CHROMEDRIVER_PATH = "C:/chromedriver/chromedriver.exe"  # prilagodi ako je na drugoj lokaciji

options = Options()
options.add_argument("--headless")  # Ne prikazuje prozor
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://example.com")
    time.sleep(2)
    print("Naslov stranice:", driver.title)
finally:
    driver.quit()
