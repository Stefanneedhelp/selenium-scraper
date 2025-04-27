import os
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TOKEN)

URL = "https://www.needhelp.com/fr/missions"
CHECK_INTERVAL = 300  # 5 minuta = 300 sekundi

def get_available_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    missions = soup.find_all("div", class_="sc-dfVpRl jymRLp")

    for mission in missions:
        title = mission.find("h2")
        location = mission.find("p", class_="sc-dkzDqf gfiVZH")
        reserved = mission.find("span", string="Réservé abonné")
        
        if reserved:
            continue  # SKOČI rezervisane poslove
        
        if title and location:
            job_text = f"{title.text.strip()} - {location.text.strip()}"
            jobs.append(job_text)
    return jobs

def main():
    print("✅ Bot pokrenut i prati ponude...")
    sent_jobs = set()

    while True:
        jobs = get_available_jobs()
        new_jobs = [job for job in jobs if job not in sent_jobs]

        if new_jobs:
            for job in new_jobs:
                bot.send_message(chat_id=CHAT_ID, text=f"🛠️ Novi posao pronađen:\n{job}")
                sent_jobs.add(job)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

