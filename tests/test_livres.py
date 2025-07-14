import pytest
from flask import session
from app import create_app
from app.models.db import db, Utilisateur, Livre, Emprunt
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test"
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_inscription_utilisateur(client):
    response = client.post("/signup", data={
        "nom": "Test",
        "email": "test@example.com",
        "mot_de_passe": "Test1234@",
        "confirmation": "Test1234@"
    }, follow_redirects=True)
    assert response.status_code == 200
    utilisateur = Utilisateur.query.filter_by(email="test@example.com").first()
    assert utilisateur is not None
    assert utilisateur.nom == "Test"

def test_connexion_utilisateur(client):
    utilisateur = Utilisateur(nom="Jean", email="jean@example.com", mot_de_passe="Mot1234!", is_admin=False)
    db.session.add(utilisateur)
    db.session.commit()

    response = client.post("/login", data={
        "email": "jean@example.com",
        "mot_de_passe": "Mot1234!"
    }, follow_redirects=True)
    assert b"Bienvenue" in response.data or response.status_code == 200

def test_ajouter_livre(client):
    livre = Livre(titre="Python 101", auteur="Guido", annee="2023", exemplaires=3)
    db.session.add(livre)
    db.session.commit()

    resultat = Livre.query.filter_by(titre="Python 101").first()
    assert resultat is not None
    assert resultat.auteur == "Guido"
    assert resultat.exemplaires == 3

def test_emprunter_livre(client):
    # Créer utilisateur + livre
    utilisateur = Utilisateur(nom="Alice", email="alice@example.com", mot_de_passe="Test1234@")
    livre = Livre(titre="SQL pour les nuls", auteur="Ben", annee="2022", exemplaires=2)
    db.session.add_all([utilisateur, livre])
    db.session.commit()

    with client.session_transaction() as sess:
        sess['utilisateur'] = {"nom": utilisateur.nom, "email": utilisateur.email, "is_admin": utilisateur.is_admin}

    response = client.post(f"/emprunter/{livre.id}", follow_redirects=True)
    assert response.status_code == 200

    emprunt = Emprunt.query.filter_by(utilisateur_email=utilisateur.email).first()
    assert emprunt is not None
    assert emprunt.livre_id == livre.id
    assert livre.exemplaires == 1  # le stock a diminué d'un

def test_modification_email(client):
    utilisateur = Utilisateur(nom="Bob", email="bob@example.com", mot_de_passe="Mot@123")
    db.session.add(utilisateur)
    db.session.commit()

    with client.session_transaction() as sess:
        sess['utilisateur'] = {"nom": utilisateur.nom, "email": utilisateur.email, "is_admin": utilisateur.is_admin}

    response = client.post("/profil", data={
        "action": "email",
        "nouveau_email": "nouveau@example.com"
    }, follow_redirects=True)

    updated = Utilisateur.query.filter_by(email="nouveau@example.com").first()
    assert updated is not None
    assert updated.email == "nouveau@example.com"
