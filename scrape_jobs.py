import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# Automatski instalira chromedriver ako ga nema
chromedriver_autoinstaller.install()

# Chrome opcije
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Pokretanje drivera
driver = webdriver.Chrome(options=options)

try:
    # 1. Otvori NeedHelp sajt
    driver.get("https://www.needhelp.com")
    time.sleep(3)

    # 2. Skrolovanje da učita sve poslove
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # 3. Filtriramo po ključnim zanimanjima
    kljucne_reci = [
        "montage", "meubles", "menuisier", "ebeniste",
        "electricite", "carrelage", "percer", "fixer",
        "enduit", "porte", "portail", "decoupe",
        "sanitaire", "parquet", "peinture"
    ]

    # 4. Nađi sve linkove poslova
    poslovi = driver.find_elements(By.TAG_NAME, "a")

    print("Nađeni odgovarajući poslovi:")
    for posao in poslovi:
        href = posao.get_attribute("href")
        if href and "needhelp.com" in href:
            for rec in kljucne_reci:
                if rec.lower() in href.lower():
                    print(href)
                    break

finally:
    driver.quit()
