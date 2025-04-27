import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

FILTER_KEYWORDS = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Béton", "Enduit", "Pose de porte, portail", "Découpe", "Pose sanitaire",
    "Pose parquet", "Peinture"
]

LAST_SEEN_JOBS = set()

def get_jobs():
    url = "https://www.needhelp.com/jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("div", class_="jobCard___StyledDiv-sc-1f6v08b-0")
    found_jobs = []

    for job in jobs:
        title_tag = job.find("h2")
        skill_tag = job.find("div", class_="tags___StyledDiv-sc-1pq4h1c-0")

        if title_tag and skill_tag:
            title = title_tag.text.strip()
            skill = skill_tag.text.strip()

            if skill in FILTER_KEYWORDS:
                link_tag = job.find("a", href=True)
                if link_tag:
                    link = "https://www.needhelp.com" + link_tag['href']
                    found_jobs.append((title, skill, link))

    return found_jobs

def main():
    while True:
        jobs = get_jobs()
        new_jobs = []

        for title, skill, link in jobs:
            if link not in LAST_SEEN_JOBS:
                LAST_SEEN_JOBS.add(link)
                new_jobs.append(f"🛠️ {title}\n🔧 {skill}\n🔗 {link}")

        if new_jobs:
            for message in new_jobs:
                bot.send_message(chat_id=CHAT_ID, text=message)
        time.sleep(300)  # 5 minuta

if __name__ == "__main__":
    main()

