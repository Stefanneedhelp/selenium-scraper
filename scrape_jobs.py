import os
import time
import requests
import shutil
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Učitaj .env varijable
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=TOKEN)

FILTERED_SKILLS = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Percer, fixer", "Enduit", "Pose de porte, portail", "Découpe",
    "Pose sanitaire", "Pose parquet", "Peinture"
]

URL = "https://www.needhelp.com/missions"
SEEN_MISSIONS = set()

# Konfiguriši Selenium
options = Options()

# Pronađi chromium binary (može biti "chromium" ili "chromium-browser")
chrome_path = shutil.which("chromium") or shutil.which("chromium-browser")
if chrome_path is None:
    raise Exception("❌ Chromium nije pronađen na sistemu!")
options.binary_location = chrome_path

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Pokreni browser
driver = webdriver.Chrome(executable_path=shutil.which("chromedriver"), options=options)


def fetch_jobs():
    driver.get(URL)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.find_all("div", class_="css-19uc56f")

    new_jobs = []
    for card in cards:
        if any(skill in card.text for skill in FILTERED_SKILLS):
            link_tag = card.find("a", href=True)
            title_tag = card.find("h2")

            if link_tag and title_tag:
                title = title_tag.text.strip()
                href = link_tag['href']
                job_id = href.split("-")[-1]

                if job_id not in SEEN_MISSIONS:
                    SEEN_MISSIONS.add(job_id)
                    full_url = f"https://www.needhelp.com{href}"
                    new_jobs.append(f"🔧 {title}\n{full_url}")
    return new_jobs_
