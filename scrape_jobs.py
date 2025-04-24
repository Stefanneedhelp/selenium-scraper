import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)

try:
    driver.get("https://example.com")
    time.sleep(2)
    print("Naslov stranice:", driver.title)
finally:
    driver.quit()
