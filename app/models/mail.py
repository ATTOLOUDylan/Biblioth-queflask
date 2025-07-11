import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Charge les variables d'environnement définies dans le fichier .env
load_dotenv()

# Fonction pour envoyer un email via SMTP sécurisé
# destinataire : l'adresse email du receveur
# sujet       : objet du message
# contenu     : corps du message
# Utilise les identifiants stockés dans les variables d'environnement MAIL_USER et MAIL_PASSWORD

def envoyer_email(destinataire, sujet, contenu):
    # Récupère l'adresse d'expédition et le mot de passe dans les variables d'environnement
    email_expediteur = os.getenv("MAIL_USER")
    mot_de_passe     = os.getenv("MAIL_PASSWORD")

    # Crée un objet de message MIME basique
    msg = EmailMessage()
    msg['Subject'] = sujet            # Objet de l'email
    msg['From']    = email_expediteur # Adresse de l'expéditeur
    msg['To']      = destinataire     # Adresse du destinataire
    msg.set_content(contenu)          # Corps du message (texte brut)

    try:
        # Établit une connexion SSL sécurisée avec le serveur SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Se connecte avec l'adresse et le mot de passe d'application
            smtp.login(email_expediteur, mot_de_passe)
            # Envoie l'email
            smtp.send_message(msg)
        print("✅ Email envoyé à", destinataire)
    except Exception as e:
        # Affiche une erreur en cas d'échec (connexion, authentification, envoi)
        print("❌ Échec d’envoi :", e)


# Point d'entrée pour tester le module en tant que script autonome
# Cela permet de valider que la configuration (.env, SMTP) fonctionne correctement
# if __name__ == "__main__":
#     envoyer_email(
 #        destinataire="ton_adresse@mail.com",  # Remplace par l'adresse de test
 #        sujet="✅ Test email sécurisé",
 #        contenu="Test réussi avec .env et python-dotenv !"
 #    )
