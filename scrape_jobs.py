import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# Lista zanimanja koje pratimo
zanimanja = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité",
    "Pose carrelage", "Percer, fixer", "Enduit", "Pose de porte, portail",
    "Découpe", "Pose sanitaire", "Pose parquet", "Peinture"
]

URL = "https://www.needhelp.com/fr/missions?available=true"

def scrape_jobs():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find_all("div", class_="task-card")  # Klasa za oglase
        novi_poslovi = []

        for job in jobs:
            title_tag = job.find("h3")
            if title_tag:
                title = title_tag.text.strip()
                for zanimanje in zanimanja:
                    if zanimanje.lower() in title.lower():
                        link_tag = job.find("a", href=True)
                        link = "https://www.needhelp.com" + link_tag["href"] if link_tag else URL
                        novi_poslovi.append(f"{title}\n{link}")
                        break

        if novi_poslovi:
            for posao in novi_poslovi:
                bot.send_message(chat_id=CHAT_ID, text=posao)
        else:
            print("Nema novih poslova.")

    except Exception as e:
        print(f"Greška pri skeniranju poslova: {e}")

def main():
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot je uspešno pokrenut na Renderu!")
    while True:
        scrape_jobs()
        time.sleep(300)  # 5 minuta

if __name__ == "__main__":
    main()




