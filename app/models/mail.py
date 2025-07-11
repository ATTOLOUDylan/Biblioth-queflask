import smtplib
from email.message import EmailMessage

def envoyer_email(destinataire, sujet, contenu):
    msg = EmailMessage()
    msg['Subject'] = sujet
    msg['From'] = "kennethattolou@gmail.com"         # ⚠️ remplace par ton email
    msg['To'] = destinataire
    msg.set_content(contenu)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("kennethattolou@gmail.com", "y z v d c u t d b m z j b i c a")  # ⚠️ Mot de passe d'application Gmail
            smtp.send_message(msg)
        print("✅ Email envoyé à", destinataire)
    except Exception as e:
        print("❌ Échec d’envoi :", e)
