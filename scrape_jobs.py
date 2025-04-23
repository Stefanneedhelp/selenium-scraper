from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Putanja do chromedriver-a (ako deploy-uješ na Render, koristiš ChromeDriver koji se instalira u runtime-u)
CHROMEDRIVER_PATH = "C:/chromedriver/chromedriver.exe"  # Lokalna putanja za testiranje

# Postavke za headless browser (za deploy na Render)
chrome_options = Options()
chrome_options.add_argument("--headless")  # bez GUI-ja
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Servis za webdriver
service = Service(CHROMEDRIVER_PATH)

# Pokretanje Chrome browsera
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Poseti sajt
    driver.get("https://example.com")
    
    # Pauza da bi se sve učitalo
    time.sleep(3)

    # Ispis naslova stranice
    print("Naslov stranice:", driver.title)

finally:
    driver.quit()
