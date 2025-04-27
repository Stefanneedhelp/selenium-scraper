import time
import os
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import chromedriver_autoinstaller

load_dotenv()

TOKEN = os.getenv("API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

chromedriver_autoinstaller.install()

keywords = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Béton", "Percer, fixer", "Découpe", "Pose sanitaire", "Pose parquet",
    "Peinture", "Enduit", "Pose de porte, portail"
]

def create_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def scrape_jobs():
    driver = create_driver()
    driver.get('https://www.needhelp.com/en/jobs')
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs_data = []

    job_elements = soup.find_all('div', class_='card-body')
    for job in job_elements:
        title_element = job.find('h2')
        link_element = job.find('a', href=True)

        if title_element and link_element:
            title = title_element.get_text(strip=True)
            link = 'https://www.needhelp.com' + link_element['href']

            if any(keyword.lower() in title.lower() for keyword in keywords):
                jobs_data.append((title, link))

    return jobs_data

def main_loop():
    sent_jobs = set()

    while True:
        try:
            jobs = scrape_jobs()
            new_jobs = [job for job in jobs if job not in sent_jobs]

            if new_jobs:
                for title, link in new_jobs:
                    message = f"🛠 Novi posao: {title}\n🔗 {link}"
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    sent_jobs.add((title, link))
            else:
                print("⏳ Nema novih poslova. Čekam 5 minuta...")

        except Exception as e:
            print(f"⚠️ Greška: {e}")

        time.sleep(300)

if __name__ == "__main__":
    main_loop()

