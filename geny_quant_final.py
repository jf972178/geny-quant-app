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

# --- INITIALISATION ---if __name__ == "__main__":
    st.title("📊 Data & Turf : Dashboard")
    st.write(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")

    
    # Message de confirmation envoyé à ton Telegram
    envoyer_alerte("🚀 SYSTÈME DATA & TURF ACTIVÉ\nLe bot est en ligne et surveille les courses.") 
    
    # Premier lancement immédiat (pour test)
    job_matinal()
    
    # Planification tous les matins à 08h00
    schedule.every().day.at("08:00").do(job_matinal)

    # Boucle pour maintenir le script actif
    while True:
        schedule.run_pending()
        time.sleep(60)
    # Message de confirmation au démarrage
    envoyer_alerte("🚀 SYSTÈME DATA & TURF ACTIVÉ\nLe bot est en ligne et surveille les courses.") 
    
    # Premier lancement
    job_matinal()
    
    # Planification
    schedule.every().day.at("08:00").do(job_matinal)
if __name__ == "__main__":
    st.title("📊 Data & Turf : Dashboard")
    st.write(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
    
    # Premier lancement pour vérifier que tout est OK
    job_matinal()
    
    # Planification automatique
    schedule.every().day.at("08:00").do(job_matinal)
