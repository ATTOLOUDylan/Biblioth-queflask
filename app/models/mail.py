# ============================================
# Script : envoyer_email.py
# But : Envoyer un email sécurisé via SMTP (Gmail)
# Usage : Peut être utilisé dans une application Flask ou en script autonome
# Sécurité : Utilise des variables d’environnement (.env) pour ne pas exposer les identifiants
# ============================================

import smtplib                    # Module pour envoyer des emails via SMTP
from email.message import EmailMessage  # Pour construire un message email bien formé
from dotenv import load_dotenv    # Pour charger les variables depuis un fichier .env
import os                         # Pour accéder aux variables d’environnement

# --------------------------------------------
# 1. Chargement des variables d’environnement
# --------------------------------------------

load_dotenv()  # Cette fonction charge automatiquement le fichier .env dans les variables système (os.environ)

# --------------------------------------------
# 2. Fonction principale pour envoyer un email
# --------------------------------------------

def envoyer_email(destinataire, sujet, contenu):
    """
    Envoie un email à un destinataire donné via SMTP sécurisé (SSL).
    
    Paramètres :
    ----------
    destinataire : str
        Adresse email du destinataire.
    sujet : str
        Sujet (objet) de l'email.
    contenu : str
        Corps (texte brut) du message à envoyer.

    Configuration requise :
    - MAIL_USER      : adresse email de l’expéditeur (dans le .env)
    - MAIL_PASSWORD  : mot de passe de l’expéditeur (mot de passe d'application Gmail)
    
    Exemple de contenu du fichier .env :
    -----------------------------------
    MAIL_USER=exemple@gmail.com
    MAIL_PASSWORD=motdepasseapplication

    Exceptions :
    - Affiche un message d’erreur si l’envoi échoue (connexion, authentification, etc.)
    """
    
    # Récupération des identifiants à partir du .env
    email_expediteur = os.getenv("MAIL_USER")
    mot_de_passe     = os.getenv("MAIL_PASSWORD")

    # Création d'un objet email standard (texte brut uniquement ici)
    msg = EmailMessage()
    msg['Subject'] = sujet
    msg['From']    = email_expediteur
    msg['To']      = destinataire
    msg.set_content(contenu)

    try:
        # Connexion sécurisée (SSL) au serveur SMTP de Gmail (port 465)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_expediteur, mot_de_passe)  # Authentification
            smtp.send_message(msg)                      # Envoi du message
        print("✅ Email envoyé à", destinataire)

    except Exception as e:
        # En cas de problème, affiche une erreur utile
        print("❌ Échec d’envoi :", e)

# --------------------------------------------
# 3. (Optionnel) Test du module en script direct
# --------------------------------------------

# Décommente ce bloc si tu veux tester ce fichier directement :
# Cela vérifie que la configuration est correcte (compte Gmail, mot de passe, .env)

# if __name__ == "__main__":
#     envoyer_email(
#         destinataire="ton_adresse@mail.com",
#         sujet="✅ Test email sécurisé",
#         contenu="Test réussi avec .env et python-dotenv !"
#     )
