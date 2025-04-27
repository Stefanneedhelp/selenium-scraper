from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

# ChromeDriver putanja koju Render koristi
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"

options = Options()
options.binary_location = GOOGLE_CHROME_BIN
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
