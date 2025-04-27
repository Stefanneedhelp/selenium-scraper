import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# Automatski instalira chromedriver ako ga nema
chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--headless")  # Ne otvara prozor
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Kreiranje drivera
driver = webdriver.Chrome(options=options)

try:
    # OVDE idemo na NeedHelp sajt
    driver.get("https://www.needhelp.com")
    time.sleep(2)
    print("Naslov stranice:", driver.title)
finally:
    driver.quit()
