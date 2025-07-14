from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Création de l'objet SQLAlchemy qui sera utilisé pour gérer la base de données
db = SQLAlchemy()

def create_app(config=None):  # Fonction de création de l'application Flask, accepte une config optionnelle
    # Charge les variables d'environnement depuis un fichier .env (ex: clés, mots de passe)
    load_dotenv()

    # Création de l'application Flask
    app = Flask(__name__)

    # Clé secrète de l'application pour sécuriser les sessions, cookies, etc.
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # Si une configuration personnalisée est passée (utile pour les tests notamment),
    # on l'applique à l'app. Sinon, on configure la base de données avec les variables d'env.
    if config:
        app.config.update(config)
    else:
        # Récupération des informations de connexion à la base de données MySQL
        user = os.getenv('MYSQL_USER')
        # Le mot de passe est encodé pour gérer les caractères spéciaux comme '@'
        password = os.getenv('MYSQL_PASSWORD').replace('@', '%40')
        host = os.getenv('MYSQL_HOST')
        db_name = os.getenv('MYSQL_DB')

        # Construction de la chaîne de connexion SQLAlchemy avec mysqlconnector
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"

        # Désactivation de la fonctionnalité de suivi des modifications pour améliorer les performances
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisation de SQLAlchemy avec l'application Flask
    db.init_app(app)

    # Import des blueprints correspondant aux différentes parties de l'application
    from app.routes.auth import auth_bp
    from app.routes.livres import livres_bp
    from app.routes.profil import profil_bp

    # Enregistrement des blueprints dans l'application
    app.register_blueprint(auth_bp)
    app.register_blueprint(livres_bp)
    app.register_blueprint(profil_bp)

    # Retourne l'objet application Flask prêt à être lancé
    return app
