import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot
from playwright.sync_api import sync_playwright

try:
    print("🔁 Pokrećem bot...")

    # Učitaj .env promenljive
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    print("📦 TOKEN:", TOKEN)
    print("📦 CHAT_ID:", CHAT_ID)

    # Provera da li su učitane vrednosti
    if not TOKEN or not CHAT_ID:
        raise ValueError("❌ TOKEN ili CHAT_ID nisu definisani!")

    bot = Bot(token=TOKEN)

    FILTERED_SKILLS = [
        "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
        "Percer, fixer", "Enduit", "Pose de porte, portail", "Découpe",
        "Pose sanitaire", "Pose parquet", "Peinture"
    ]

    URL = "https://www.needhelp.com/missions"
    SEEN_MISSIONS = set()

    def fetch_jobs():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL)
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")
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
        return new_jobs

    def main():
        bot.send_message(chat_id=CHAT_ID, text="✅ Playwright bot pokrenut na Renderu!")

        while True:
            jobs = fetch_jobs()
            if jobs:
                for job in jobs:
                    bot.send_message(chat_id=CHAT_ID, text=job)
            time.sleep(300)

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ Fatalna greška: {e}")
    try:
        if 'bot' in locals() and CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=f"❌ Fatalna greška:\n{e}")
    except Exception as telegram_error:
        print(f"⚠️ Neuspešno slanje greške na Telegram: {telegram_error}")
