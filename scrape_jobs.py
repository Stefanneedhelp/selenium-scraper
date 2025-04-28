Build fix - trigger deploy
import time
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from dotenv import load_dotenv
import telegram

# Učitaj .env varijable
load_dotenv()
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Inicijalizuj Telegram bota
bot = telegram.Bot(token=TOKEN)

# Automatski instaliraj chromedriver
chromedriver_autoinstaller.install()

# Selenium opcije
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Pravi driver
driver = webdriver.Chrome(options=chrome_options)

# Sajt koji proveravamo
URL = "https://www.needhelp.com/"

# Filter zanimanja koje tražimo
DOZVOLJENE_KATEGORIJE = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage", 
    "Percer, fixer", "Découpe", "Pose sanitaire", "Pose parquet", "Peinture",
    "Enduit", "Pose de porte, portail"
]

# Funkcija za proveru novih poslova
def proveri_poslove():
    try:
        driver.get(URL)
        time.sleep(5)  # Sačekaj da se stranica učita

        soup = BeautifulSoup(driver.page_source, "html.parser")
        poslovi = soup.find_all("div", class_="job-card")  # Primer klasa, izmeni ako treba

        novi_poslovi = []

        for posao in poslovi:
            kategorija = posao.find("div", class_="job-category")  # Primer klasa
            if kategorija and kategorija.text.strip() in DOZVOLJENE_KATEGORIJE:
                naslov = posao.find("h2").text.strip()
                lokacija = posao.find("div", class_="job-location").text.strip()
                cena = posao.find("div", class_="job-price").text.strip()

                novi_poslovi.append(f"🔔 Novi posao: {naslov}\n📍 Lokacija: {lokacija}\n💶 Cena: {cena}")

        if novi_poslovi:
            for posao in novi_poslovi:
                bot.send_message(chat_id=CHAT_ID, text=posao)
        else:
            print("Nema novih poslova.")
    except Exception as e:
        print(f"Greška prilikom provere poslova: {e}")

# Pošalji poruku da je bot startovan
bot.send_message(chat_id=CHAT_ID, text="✅ Bot je pokrenut i proverava poslove!")

# Glavna petlja
while True:
    proveri_poslove()
    time.sleep(300)  # Pauza 5 minuta
