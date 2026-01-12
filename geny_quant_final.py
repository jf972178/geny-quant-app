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
    print(f"--- Scan Geny lancé à {datetime.now().strftime('%H:%M')} ---")
    
    try:
        # Simulation de scan pour le test de Lundi
        found = False 
        if not found:
            print("Aucune cible détectée pour le moment.")
    except Exception as e:
        print(f"Erreur technique : {e}")

# --- INITIALISATION ET SURVEILLANCE ---
if __name__ == "__main__":
    st.title("📊 Data & Turf : Dashboard")
    st.write(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. Message de confirmation immédiat
    envoyer_alerte("🚀 SYSTÈME DATA & TURF ACTIVÉ\nLe bot est prêt pour le scan de demain 08h00.") 
    
    # 2. Lancement du premier scan
    job_matinal()
    
    # 3. Programmation
    schedule.every().day.at("08:00").do(job_matinal)

    while True:
        schedule.run_pending()
        time.sleep(60)
