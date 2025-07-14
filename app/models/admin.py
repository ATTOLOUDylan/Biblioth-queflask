from app import db
from app.models.db import Utilisateur

# Fonction pour créer un compte administrateur par défaut
def creer_admin():
    """
    Crée un compte admin SEULEMENT s'il n'en existe aucun (is_admin = True).
    """
    email_admin = "admin@gmail.com"
    mot_de_passe_admin = "admin2005"
    nom_admin = "Admin"

    # Vérifie s'il existe déjà un administrateur
    admin_existant = Utilisateur.query.filter_by(is_admin=True).first()

    if admin_existant:
        print(f"ℹ️ Un administrateur existe déjà (email : {admin_existant.email})")
    else:
        nouvel_admin = Utilisateur(
            nom=nom_admin,
            email=email_admin,
            mot_de_passe=mot_de_passe_admin,
            is_admin=True
        )
        db.session.add(nouvel_admin)
        db.session.commit()
        print(f"✅ Admin créé : {email_admin} / {mot_de_passe_admin}")
