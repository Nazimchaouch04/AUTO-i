import requests
import logging
from decouple import config
from .models import CanalNotification, NotificationHistory

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

def envoyer_message_telegram(chat_id, message):
    """Envoie un message Telegram."""
    if not TELEGRAM_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN non configuré - Simulation du message")
        print(f"Telegram vers {chat_id}: {message[:100]}...")
        return True
    
    url = f'{TELEGRAM_API}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('ok'):
            logger.info(f"Message Telegram envoyé à {chat_id}")
            return True
        else:
            error_msg = result.get('description', 'Erreur inconnue')
            logger.error(f"Erreur API Telegram: {error_msg}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur requête Telegram: {e}")
        return False
    except Exception as e:
        logger.error(f"Erreur inattendue Telegram: {e}")
        return False

def formater_alerte_telegram(annonce, alerte):
    """Formate un message d'alerte Telegram."""
    ecart_str = ''
    if annonce.ecart_prix and annonce.ecart_prix < 0:
        ecart_str = f'🔥 <b>{abs(annonce.ecart_prix):.0f}% sous le marché</b>\n'
    
    # Formatage du prix
    prix_str = f"{annonce.prix:,.0f} €".replace(',', ' ')
    
    # Formatage du kilométrage
    km_str = f"{annonce.kilometrage:,} km".replace(',', ' ')
    
    # Estimation si disponible
    estimation_str = ""
    if annonce.prix_estime:
        estime_str = f"{annonce.prix_estime:,.0f} €".replace(',', ' ')
        estimation_str = f"\n📊 Estimation marché : {estime_str}"
    
    # URL de l'annonce
    annonce_url = f"https://autointel.vercel.app/annonces/{annonce.id}"
    
    message = f"""🚗 <b>Nouvelle bonne affaire !</b>

{ecart_str}<b>{annonce.vehicule.marque} {annonce.vehicule.modele} {annonce.annee}</b>
💰 Prix : <b>{prix_str}</b>
📍 {annonce.ville or 'Non précisé'} · {annonce.pays}
🛣️ {km_str} · {annonce.carburant}{estimation_str}

🔗 Voir sur AutoIntel : {annonce_url}

<i>Alerte : {alerte.nom}</i>"""
    
    return message

def verifier_chat_id(chat_id):
    """Vérifie si un chat_id Telegram est valide."""
    if not TELEGRAM_TOKEN:
        return True  # Simulation mode
    
    url = f'{TELEGRAM_API}/getChat'
    payload = {'chat_id': chat_id}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result.get('ok', False)
    except:
        return False

def envoyer_message_test_telegram(chat_id):
    """Envoie un message de test pour vérifier la connexion."""
    message = """🤖 <b>Test AutoIntel</b>

✅ Votre bot Telegram est bien connecté !

Vous recevrez maintenant les alertes de bonnes affaires directement ici.

<i>Configuration terminée avec succès !</i>"""
    
    return envoyer_message_telegram(chat_id, message)

def get_bot_info():
    """Récupère les informations du bot Telegram."""
    if not TELEGRAM_TOKEN:
        return None
    
    url = f'{TELEGRAM_API}/getMe'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get('ok'):
            return result.get('result')
        return None
    except:
        return None
