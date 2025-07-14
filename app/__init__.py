from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(config=None):  # 👈 accepte un paramètre
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    # 👉 Applique une configuration personnalisée si fournie (utile pour les tests)
    if config:
        app.config.update(config)
    else:
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD').replace('@', '%40')
        host = os.getenv('MYSQL_HOST')
        db_name = os.getenv('MYSQL_DB')

        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.livres import livres_bp
    from app.routes.profil import profil_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(livres_bp)
    app.register_blueprint(profil_bp)

    return app
