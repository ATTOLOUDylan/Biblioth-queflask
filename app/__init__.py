# app/__init__.py
from flask import Flask
from app.models.db import creer_base
from app.models.admin import creer_admin

def create_app():
    app = Flask(__name__)
    app.secret_key = 'cle-secrete-dylan'

    # Initialisation base + admin
    creer_base()
    creer_admin()

    # Importer les routes
    from app.routes.auth import auth_bp
    from app.routes.livres import livres_bp
    from app.routes.profil import profil_bp

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(livres_bp)
    app.register_blueprint(profil_bp)

    return app
