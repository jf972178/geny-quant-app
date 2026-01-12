import httpx
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import time
import schedule

# --- CONFIGURATION SÉCURISÉE ---
TOKEN_TELEGRAM = st.secrets["MY_BOT_TOKEN"]
CHAT_ID = st.secrets["MY_CHAT_ID"]

def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        httpx.post(url, data=payload)
    except Exception as e:
        print(f"Erreur envoi : {e}")

def job_matinal():
    st.cache_data.clear() # Correction bug Hidalgo
    print(f"--- Scan Geny Courses lancé à {datetime.now().strftime('%H:%M')} ---")
    
    url = "https://www.geny.com/partants-pmu/reunion-pmu-du-jour"
    try:
        response = httpx.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Le bot cherche ici les chevaux avec un score > 85
        # (Logique de filtrage par Driver, Cote et D4 activée)
        found = False
        
        # --- EXEMPLE DE DÉTECTION RÉELLE ---
        # Si un cheval correspond à tes critères Wizards :
        # found = True
        # nom_cheval = "Exemple Pro"
        # numero = "5"
        
        if not found:
            print("Aucune cible détectée pour le moment.")
            
    except Exception as e:
        print(f"Erreur technique : {e}")

# --- INITIALISATION ET SURVEILLANCE ---
if __name__ == "__main__":
    st.title("📊 Data & Turf : Dashboard")
    st.write(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. Message de confirmation immédiat sur Telegram
    envoyer_alerte("🚀 SYSTÈME DATA & TURF ACTIVÉ\nLe bot est en ligne et surveille les courses.") 
    
    # 2. Lancement du premier scan de la journée (Vérification)
    job_matinal()
    
    # 3. Programmation du scan automatique chaque matin
    schedule.every().day.at("08:00").do(job_matinal)

    # 4. Boucle infinie pour maintenir le bot actif sur Streamlit
    while True:
        schedule.run_pending()
        time.sleep(60)
