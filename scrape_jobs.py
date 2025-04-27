import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Učitaj .env fajl
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Tvoj sajt
URL = "https://www.needhelp.com/en-gb/listing"

# Koje ključne reči filtriramo
KEYWORDS = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Percer, fixer", "Découpe", "Pose sanitaire", "Pose parquet",
    "Enduit", "Peinture", "Pose de porte, portail"
]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def scrape_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service("/usr/bin/chromedriver")  # Render koristi ovaj path

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(URL)
        time.sleep(3)  # Sačekaj da se sve učita

        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = soup.find_all("div", class_="taskCard--details")

        for job in jobs:
            title = job.find("h2")
            if title:
                title_text = title.get_text().strip()
                if any(keyword.lower() in title_text.lower() for keyword in KEYWORDS):
                    link = "https://www.needhelp.com" + job.find("a")["href"]
                    message = f"<b>{title_text}</b>\n{link}"
                    send_telegram_message(message)

    finally:
        driver.quit()

if __name__ == "__main__":
    while True:
        scrape_jobs()
        print("✅ Provereno! Čeka sledećih 30 minuta...")
        time.sleep(1800)  # 30 minuta

