from app import db
from datetime import datetime

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mot_de_passe = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Livre(db.Model):
    __tablename__ = 'livres'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    auteur = db.Column(db.String(255), nullable=False)
    annee = db.Column(db.String(4), nullable=False)
    exemplaires = db.Column(db.Integer, default=1)

class Emprunt(db.Model):
    __tablename__ = 'emprunts'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_email = db.Column(db.String(255), db.ForeignKey('utilisateurs.email'))
    livre_id = db.Column(db.Integer, db.ForeignKey('livres.id'))
    date_emprunt = db.Column(db.DateTime, default=datetime.utcnow)
    date_limite = db.Column(db.Date)
