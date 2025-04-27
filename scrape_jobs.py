
import os
import time
import requests
from bs4 import BeautifulSoup
import telegram
from dotenv import load_dotenv

# Učitavanje .env varijabli
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

# 🛎️ Pošalji obaveštenje kad bot krene
bot.send_message(chat_id=CHAT_ID, text="✅ Bot je uspešno pokrenut na Renderu!")

# URL sajta
URL = "https://www.needhelp.com/profils"

# Lista dozvoljenih zanimanja
DOZVOLJENA_ZANIMANJA = [
    "Montage de meubles", "Menuisier, ébéniste", "Électricité", "Pose carrelage",
    "Percer, fixer", "Découpe", "Pose sanitaire", "Pose parquet", "Peinture", 
    "Enduit", "Pose de porte, portail"
]

# Set za čuvanje već viđenih poslova
vidjeni_poslovi = set()

def pronadji_poslove():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        poslovi = soup.find_all("div", class_="profile-card")  # ← prilagodi ako treba
        
        novi_poslovi = []

        for posao in poslovi:
            naziv_element = posao.find("h2")
            kategorija_element = posao.find("div", class_="profile-skills")

            if naziv_element and kategorija_element:
                naziv = naziv_element.text.strip()
                kategorija = kategorija_element.text.strip()

                # Provera da li je zanimanje na listi
                if any(dozvoljeno in kategorija for dozvoljeno in DOZVOLJENA_ZANIMANJA):
                    if naziv not in vidjeni_poslovi:
                        vidjeni_poslovi.add(naziv)
                        novi_poslovi.append(f"🔹 {naziv} - {kategorija}")

        return novi_poslovi

    except Exception as e:
        print(f"Greška prilikom pronalaženja poslova: {e}")
        return []

# Glavna petlja
while True:
    novi_poslovi = pronadji_poslove()

    if novi_poslovi:
        for posao in novi_poslovi:
            bot.send_message(chat_id=CHAT_ID, text=posao)
    else:
        print("Nema novih poslova trenutno.")  # Ne šaljemo poruku ako nema novih

    time.sleep(300)  # 5 minuta pauze
