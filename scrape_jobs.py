import os
import time
import telegram
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# Učitavanje .env fajla
load_dotenv()

# Uzimanje podataka iz .env
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Podesavanje Chrome drivera
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service()  # automatski koristi instalirani driver
driver = webdriver.Chrome(service=service, options=options)

def scrape_jobs():
    url = "https://www.needhelp.com/pro/search"  # <-- ovde pravi link na NeedHelp
    driver.get(url)
    time.sleep(3)  # čekanje da se stranica učita

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("div", class_="job-offer-card-content")

    filtered_jobs = []

    keywords = [
        "Montage de meubles",
        "Menuisier, ébéniste",
        "Électricité",
        "Pose carrelage",
        "Enduit",
        "Pose de porte, portail",
        "Percer, fixer",
        "Découpe",
        "Pose sanitaire",
        "Pose parquet",
        "Peinture"
    ]

    for job in jobs:
        title = job.get_text(strip=True)
        if any(keyword.lower() in title.lower() for keyword in keywords):
            filtered_jobs.append(title)

    return filtered_jobs

def send_to_telegram(message):
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    try:
        jobs = scrape_jobs()
        if jobs:
            for job in jobs:
                send_to_telegram(f"Nova ponuda: {job}")
        else:
            send_to_telegram("Nema novih poslova za danas.")
    except Exception as e:
        send_to_telegram(f"Bot error: {e}")
    finally:
        driver.quit()


