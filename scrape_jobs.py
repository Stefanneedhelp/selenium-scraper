import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from telegram import Bot

# Ucitaj .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Podesi Telegram bot
bot = Bot(token=TOKEN)

def send_telegram_message(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def get_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.needhelp.com/fr-fr/missions"
    driver.get(url)

    time.sleep(5)  # Sacekaj da se stranica ucita

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    job_cards = soup.find_all("div", class_="missions-card")

    jobs = []

    for card in job_cards:
        title_element = card.find("div", class_="title")
        location_element = card.find("div", class_="localization")
        budget_element = card.find("div", class_="budget")

        if title_element and location_element and budget_element:
            title = title_element.get_text(strip=True)
            location = location_element.get_text(strip=True)
            budget = budget_element.get_text(strip=True)

            job_info = f"{title} | {location} | {budget}"
            jobs.append(job_info)

    return jobs

def main():
    sent_jobs = set()

    while True:
        try:
            jobs = get_jobs()

            if not jobs:
                print("Nema novih poslova.")
            else:
                for job in jobs:
                    if job not in sent_jobs:
                        send_telegram_message(f"Novi posao: {job}")
                        sent_jobs.add(job)

            time.sleep(300)  # Pauza 5 minuta

        except Exception as e:
            print(f"Greska: {e}")
            time.sleep(60)  # Ako padne, cekaj 1 minutu pa pokusaj opet

if __name__ == "__main__":
    send_telegram_message("✅ Bot je uspešno pokrenut na Renderu!")
    main()

