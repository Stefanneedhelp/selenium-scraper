import os
import time
import telegram
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Učitavanje .env varijabli
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TOKEN)

# Auto instalacija ChromeDriver-a
chromedriver_autoinstaller.install()

# Podesavanje za Render server
options = Options()
options.binary_location = "/usr/bin/chromium-browser"
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Otvaranje stranice
    driver.get("https://www.needhelp.com/en/jobs")
    time.sleep(2)

    # Parsiranje HTML-a
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Traženje svih poslova
    jobs = soup.find_all("div", class_="job-card")

    # Lista zanimanja koje pratiš
    keywords = [
        "Montage de meubles",
        "Menuisier, ébéniste",
        "Électricité",
        "Pose carrelage",
        "Béton",
        "Percer, fixer",
        "Enduit",
        "Pose de porte, portail",
        "Découpe",
        "Pose sanitaire",
        "Pose parquet",
        "Peinture"
    ]

    # Slanje poslova na Telegram
    for job in jobs:
        job_title = job.text.strip()
        for keyword in keywords:
            if keyword.lower() in job_title.lower():
                bot.send_message(chat_id=CHAT_ID, text=f"🛠 Novi posao: {job_title}")
                break

finally:
    driver.quit()
