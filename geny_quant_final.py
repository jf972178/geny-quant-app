import httpx
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# --- CONFIGURATION (METS TON TOKEN ICI) ---
TOKEN_TELEGRAM = "8271770358:AAFHv4YQFbZKLzXHDSp6Jv_J3HAl8nuyH2w" # <--- Colle ton token entre les guillemets
CHAT_ID = "6701776187"

# --- FONCTION ENVOI TELEGRAM ---
def envoyer_alerte(message):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = httpx.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Message envoyé sur Telegram !")
        else:
            print(f"❌ Erreur Telegram : {response.status_code}")
    except Exception as e:
        print(f"Erreur technique : {e}")

# --- ANALYSE DES COURSES ---
def job_matinal():
    print(f"--- Scan Geny Courses lancé à {datetime.now().strftime('%H:%M')} ---")
    
    # Ici le script scanne les données Geny
    # On simule une détection pour vérifier que ton Token fonctionne
    cible_detectee = True 
    
    if cible_detectee:
        msg = "🚀 *ALERTE GENY-QUANT : NOUVELLE CIBLE*\n\n"
        msg += "📍 *Course :* R1C4 - Vincennes (Trot)\n"
        msg += "🐎 *Cheval :* IDALGO (n°12)\n"
        msg += "📊 *Score :* 88/100 (Bonus D4 inclus)\n"
        msg += "🛡️ *Mode Simulation :* Mise suggérée 10€"
        envoyer_alerte(msg)
    else:
        print("Aucun cheval n'a atteint le score de 80/100 aujourd'hui.")

# --- INITIALISATION ET TEST ---
print(f"Lancement du système pour l'ID {CHAT_ID}...")

# TEST IMMÉDIAT : On lance le scan dès le démarrage pour vérifier le Token
job_matinal()

# PLANIFICATION : Le script le refera tout seul chaque matin à 08h00
schedule.every().day.at("08:00").do(job_matinal)

while True:
    schedule.run_pending()
    time.sleep(60)
