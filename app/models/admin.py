# ============================================
# Script : creer_admin.py
# But : Créer un compte administrateur par défaut dans la base de données,
#       uniquement s’il n’en existe aucun.
# Usage : Ce script peut être appelé manuellement ou automatiquement 
#         au démarrage de l'application Flask.
# ============================================

# Importation de l'objet db (SQLAlchemy) depuis le module principal de l'application
from app import db

# Importation du modèle Utilisateur qui contient les informations des utilisateurs
from app.models.db import Utilisateur


def creer_admin():
    """
    Crée un compte administrateur par défaut dans la base de données.

    Cette fonction vérifie s'il existe déjà un utilisateur avec le rôle d'administrateur
    (is_admin=True). Si ce n’est pas le cas, elle crée un utilisateur avec les 
    informations suivantes :
    
        - Nom : Admin
        - Email : admin@gmail.com
        - Mot de passe : admin2005
        - Rôle : Administrateur (is_admin=True)
    
    ⚠️ Avertissement :
    - Le mot de passe est en clair ici. Il est recommandé d'utiliser un système de hachage 
      sécurisé (comme bcrypt ou werkzeug.security).
    - Cette fonction ne devrait être appelée qu'une seule fois (par exemple au démarrage 
      de l'application) pour garantir qu’un administrateur est disponible.

    Retour :
        Aucun retour (affiche un message dans le terminal).
    """

    # Données du compte admin à créer
    email_admin = "admin@gmail.com"
    mot_de_passe_admin = "admin2005"
    nom_admin = "Admin"

    # Vérifie si un administrateur existe déjà dans la base
    admin_existant = Utilisateur.query.filter_by(is_admin=True).first()

    if admin_existant:
        # Si un admin existe déjà, on informe l'utilisateur
        print(f"ℹ️ Un administrateur existe déjà (email : {admin_existant.email})")
    else:
        # Création d’un nouvel utilisateur avec les droits administrateurs
        nouvel_admin = Utilisateur(
            nom=nom_admin,
            email=email_admin,
            mot_de_passe=mot_de_passe_admin,  # ⚠️ En clair : à améliorer
            is_admin=True
        )

        # Sauvegarde du nouvel admin dans la base de données
        db.session.add(nouvel_admin)
        db.session.commit()

        # Affichage d'un message de confirmation dans la console
        print(f"✅ Admin créé : {email_admin} / {mot_de_passe_admin}")
