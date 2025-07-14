# app/__init__.py

from flask import Flask
from app.models.db import db
from app.routes.auth import auth_bp
from app.routes.livres import livres_bp
from app.routes.profil import profil_bp

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configuration par défaut
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/test_bibliotheque'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True  # Active le mode test
    
    # Surcharge si test_config est fourni
    if test_config:
        app.config.update(test_config)

    # Initialiser la base
    db.init_app(app)

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(livres_bp)
    app.register_blueprint(profil_bp)

    return app
