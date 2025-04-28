import time
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from telegram import Bot

# Ucitaj .env varijable
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Podesi Telegram bota
bot = Bot(token=TOKEN)

# Konfiguracija za Chromium browser
options = Options()
options.binary_location = '/usr/bin/chromium-browser'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Pokreni driver
driver = webdriver.Chrome(options=options)

# Lista kategorija koje nas zanimaju
ZANIMANJA = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Percer, fixer", "Découpe", "Pose sanitaire", "Pose parquet",
    "Peinture", "Enduit", "Pose de porte, portail"
]

# Funkcija za slanje poruke

def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

# Funkcija za proveru poslova

def scrape_jobs():
    driver.get("https://www.needhelp.com/fr-fr/missions")
    time.sleep(5)  # Sačekaj da se stranica ucita

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="missions-card")

    novi_poslovi = []

    for posao in job_cards:
        title_tag = posao.find("div", class_="title")
        if title_tag:
            title = title_tag.text.strip()
            for zanimanje in ZANIMANJA:
                if zanimanje.lower() in title.lower():
                    link_tag = posao.find("a", href=True)
                    link = "https://www.needhelp.com" + link_tag['href'] if link_tag else "https://www.needhelp.com/fr-fr/missions"
                    message = f"🔔 Novi posao: {title}\n➡️ Link: {link}"
                    novi_poslovi.append(message)
                    break

    return novi_poslovi

# Glavna funkcija

def main():
    poslati_poslovi = set()

    send_telegram_message("✅ Bot je uspešno pokrenut na Renderu!")

    while True:
        try:
            novi_poslovi = scrape_jobs()

            for posao in novi_poslovi:
                if posao not in poslati_poslovi:
                    send_telegram_message(posao)
                    poslati_poslovi.add(posao)

            time.sleep(300)  # Cekaj 5 minuta

        except Exception as e:
            print(f"Greska u radu bota: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()

