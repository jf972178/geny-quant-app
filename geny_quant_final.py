import httpx
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import time
import schedule

# --- CONFIGURATION ---
TOKEN_TELEGRAM = st.secrets["MY_BOT_TOKEN"]
CHAT_ID = st.secrets["MY_CHAT_ID"]

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        httpx.post(url, data=payload)
    except Exception as e:
        print(f"Erreur envoi Telegram : {e}")

def job_matinal():
    st.cache_data.clear()
    print(f"--- Scan Geny lancé le {datetime.now().strftime('%d/%m à %H:%M')} ---")
    
    url = "https://www.geny.com/partants-pmu/reunion-pmu-du-jour"
    try:
        with httpx.Client(timeout=15.0) as client:
            response = client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            cibles = []
            
            # --- LOGIQUE DE DÉTECTION ---
            courses = soup.find_all('div', class_='pmu-course')
            for course in courses:
                nom_c = course.find('h3').text.strip()
                partants = course.find_all('tr', class_='partant')
                for p in partants:
                    score = 80 # Base de confiance
                    if "D4" in p.text: score += 10 # Bonus déferrage
                    
                    if score >= 85: # Seuil de mise
                        cibles.append({'c': nom_c, 'n': p.find('td', class_='nom').text.strip(), 's': score})

            if cibles:
                for cb in cibles:
                    msg = f"🚀 *CIBLE DÉTECTÉE*\n📍 {cb['c']}\n🐎 {cb['n']}\n📊 Score : {cb['s']}/100\n💰 Mise : 10€"
                    envoyer_alerte(msg)
            else:
                print("Aucun cheval à 85/100 aujourd'hui.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    st.title("📊 Data & Turf : Dashboard")
    st.write(f"Dernière vérification : {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. Message de confirmation (uniquement au premier démarrage)
    # envoyer_alerte("✅ SYSTÈME OPÉRATIONNEL\nPrêt pour le scan de demain 08h00.")

    # 2. LANCEMENT DU SCAN
    # On lance le scan à chaque fois que l'application est réveillée par Cron-job
    job_matinal()
  
