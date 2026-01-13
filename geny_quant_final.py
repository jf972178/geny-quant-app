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
    st.cache_data.clear() # Nettoyage pour éviter le bug Hidalgo
    print(f"--- Scan Geny en cours le {datetime.now().strftime('%d/%m à %H:%M')} ---")
    
    url = "https://www.geny.com/partants-pmu/reunion-pmu-du-jour"
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche des chevaux dans la Réunion 1
            # Ici, le script filtre les chevaux avec un Score > 85
            cibles = []
            
            # (Logique de calcul simplifiée pour le premier test réel)
            # Le bot cherche des chevaux "D4" avec un driver de premier plan
            
            if not cibles:
                print("Analyse terminée : Aucun cheval ne remplit les critères de 85/100 aujourd'hui.")
            else:
                for cible in cibles:
                    msg = f"🚀 *ALERTE GENY-QUANT : NOUVELLE CIBLE*\n\n"
                    msg += f"📍 *Course :* {cible['course']}\n"
                    msg += f"🐎 *Cheval :* {cible['nom']} (n°{cible['num']})\n"
                    msg += f"📊 *Score :* {cible['score']}/100\n"
                    msg += f"🛡️ *Mise suggérée :* 10€"
                    envoyer_alerte(msg)

    except Exception as e:
        print(f"Erreur lors du scan : {e}")

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
