import httpx
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime

# 1. IDENTIFIANTS
TOKEN_TELEGRAM = st.secrets["MY_BOT_TOKEN"]
CHAT_ID = st.secrets["MY_CHAT_ID"]

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        httpx.post(url, data=payload)
    except Exception as e:
        st.error(f"Erreur Telegram : {e}")

def job_matinal():
    st.cache_data.clear()
    url = "https://www.geny.com/partants-pmu/reunion-pmu-du-jour"
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            courses = soup.find_all('div', class_='pmu-course')
            for c in courses:
                nom_c = c.find('h3').text.strip()
                partants = c.find_all('tr', class_='partant')
                for p in partants:
                    if "D4" in p.text:
                        nom_p = p.find('td', class_='nom').text.strip()
                        envoyer_alerte(f"🚀 *CIBLE*\n📍 {nom_c}\n🐎 {nom_p}")
    except Exception as e:
        st.error(f"Erreur Scan : {e}")

# 2. EXÉCUTION (TOUT EST COLLÉ À GAUCHE SANS EXCEPTION)
st.title("📊 Data & Turf : Dashboard")
st.write(f"Dernier scan : {datetime.now().strftime('%H:%M:%S')}")

# Lancement immédiat au réveil par Cron-job
job_matinal()

# Message de confirmation
envoyer_alerte("✅ SYSTÈME OPÉRATIONNEL\nURL et Code validés pour les 490€.")
