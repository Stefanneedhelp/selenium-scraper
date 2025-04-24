import undetected_chromedriver as uc
import time

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# NE postavljaj binary_location, Render će automatski naći browser
driver = uc.Chrome(options=options, use_subprocess=True)

try:
    driver.get("https://example.com")
    time.sleep(2)
    print("Naslov stranice:", driver.title)
finally:
    driver.quit()
