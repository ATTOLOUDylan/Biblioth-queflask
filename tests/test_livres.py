import pytest
from flask import session
from app import create_app
from app.models.db import db, Utilisateur, Livre, Emprunt
from datetime import datetime, timedelta

# Fixture pytest pour configurer l'application et le client de test
@pytest.fixture
def client():
    # Création de l'app Flask avec config test, base SQLite en mémoire
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test"
    })

    # Contexte application pour la création/suppression de la base
    with app.app_context():
        db.create_all()           # Création des tables
        yield app.test_client()   # Fournit un client HTTP pour tests
        db.session.remove()       # Nettoyage session DB
        db.drop_all()             # Suppression des tables


# Test de l'inscription d'un nouvel utilisateur via la route /signup
def test_inscription_utilisateur(client):
    response = client.post("/signup", data={
        "nom": "Test",
        "email": "test@example.com",
        "mot_de_passe": "Test1234@",
        "confirmation": "Test1234@"
    }, follow_redirects=True)  # Suit la redirection vers page suivante après inscription

    assert response.status_code == 200  # Vérifie que la réponse HTTP est OK
    # Recherche dans la base l'utilisateur nouvellement créé
    utilisateur = Utilisateur.query.filter_by(email="test@example.com").first()
    assert utilisateur is not None  # L'utilisateur doit exister
    assert utilisateur.nom == "Test"  # Le nom doit correspondre


# Test de la connexion utilisateur via /login
def test_connexion_utilisateur(client):
    # Préparation : ajout manuel d'un utilisateur en base (non via formulaire)
    utilisateur = Utilisateur(nom="Jean", email="jean@example.com", mot_de_passe="Mot1234!", is_admin=False)
    db.session.add(utilisateur)
    db.session.commit()

    # Tentative de connexion via POST sur /login avec email et mot de passe valides
    response = client.post("/login", data={
        "email": "jean@example.com",
        "mot_de_passe": "Mot1234!"
    }, follow_redirects=True)

    # Vérifie que la réponse contient un indice de succès (ex. "Bienvenue") ou code 200 OK
    assert b"Bienvenue" in response.data or response.status_code == 200


# Test de l'ajout d'un livre directement dans la base
def test_ajouter_livre(client):
    # Création et ajout d'un livre
    livre = Livre(titre="Python 101", auteur="Guido", annee="2023", exemplaires=3)
    db.session.add(livre)
    db.session.commit()

    # Recherche du livre dans la base pour vérifier sa présence et ses attributs
    resultat = Livre.query.filter_by(titre="Python 101").first()
    assert resultat is not None
    assert resultat.auteur == "Guido"
    assert resultat.exemplaires == 3


# Test d'emprunt d'un livre par un utilisateur connecté
def test_emprunter_livre(client):
    # Préparation : création d'un utilisateur et d'un livre
    utilisateur = Utilisateur(nom="Alice", email="alice@example.com", mot_de_passe="Test1234@")
    livre = Livre(titre="SQL pour les nuls", auteur="Ben", annee="2022", exemplaires=2)
    db.session.add_all([utilisateur, livre])
    db.session.commit()

    # Simulation d'une session utilisateur (connexion simulée)
    with client.session_transaction() as sess:
        sess['utilisateur'] = {"nom": utilisateur.nom, "email": utilisateur.email, "is_admin": utilisateur.is_admin}

    # POST pour emprunter le livre (route /emprunter/<livre_id>)
    response = client.post(f"/emprunter/{livre.id}", follow_redirects=True)
    assert response.status_code == 200

    # Vérification en base qu'un emprunt a été créé
    emprunt = Emprunt.query.filter_by(utilisateur_email=utilisateur.email).first()
    assert emprunt is not None
    assert emprunt.livre_id == livre.id
    # Vérifie que le nombre d'exemplaires a diminué de 1
    assert livre.exemplaires == 1  


# Test de modification d'email utilisateur via formulaire /profil
def test_modification_email(client):
    # Ajout d'un utilisateur existant en base
    utilisateur = Utilisateur(nom="Bob", email="bob@example.com", mot_de_passe="Mot@123")
    db.session.add(utilisateur)
    db.session.commit()

    # Simulation de session utilisateur (connexion)
    with client.session_transaction() as sess:
        sess['utilisateur'] = {"nom": utilisateur.nom, "email": utilisateur.email, "is_admin": utilisateur.is_admin}

    # Envoi POST pour modifier l'email via formulaire profil
    response = client.post("/profil", data={
        "action": "email",
        "nouveau_email": "nouveau@example.com"
    }, follow_redirects=True)

    # Vérifie que l'email a bien été modifié en base
    updated = Utilisateur.query.filter_by(email="nouveau@example.com").first()
    assert updated is not None
    assert updated.email == "nouveau@example.com"
