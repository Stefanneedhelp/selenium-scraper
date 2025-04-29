import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ✅ Putanja do Chromium browsera na Render serveru
CHROME_PATH = "/usr/bin/chromium-browser"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

options = Options()
options.binary_location = CHROME_PATH
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# ✅ Poslovi koji su već poslati
sent_jobs = set()

# ✅ Zanimanja koja želiš da pratiš
KEYWORDS = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité",
    "Pose carrelage", "Enduit", "Pose de porte, portail",
    "Percer, fixer", "Découpe", "Pose sanitaire",
    "Pose parquet", "Peinture"
]

def check_jobs():
    global sent_jobs
    driver.get("https://www.needhelp.com/")

    time.sleep(3)  # sačekaj da se stranica učita

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("div", class_="card-body")

    found = False
    for job in jobs:
        title_tag = job.find("h2")
        if title_tag:
            title = title_tag.get_text(strip=True)
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                if title not in sent_jobs:
                    link = "https://www.needhelp.com" + job.find("a")["href"]
                    message = f"🔨 Novi posao: {title}\n{link}"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    sent_jobs.add(title)
                    found = True

    if not found:
        print("Nema novih poslova za slanje.")

# ✅ Glavna petlja
if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot je uspešno pokrenut na Renderu!")
    while True:
        check_jobs()
        time.sleep(300)  # proverava na svakih 5 minuta


