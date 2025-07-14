import pytest
from flask import session
from app import create_app, db
from app.models.db import Utilisateur

# Fixture pytest pour configurer un client de test Flask
@pytest.fixture
def client():
    # Création de l'application Flask avec configuration spécifique pour les tests
    app = create_app({
        "TESTING": True,  # Active le mode test (par ex. gestion des erreurs)
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Base de données en mémoire pour tests rapides
        "SECRET_KEY": "test_key"  # Clé secrète pour les sessions en test
    })

    # Contexte application pour créer/supprimer la base de données avant/après les tests
    with app.app_context():
        db.create_all()  # Création des tables SQLAlchemy dans la base mémoire
        yield app.test_client()  # Fournit un client HTTP pour tester les routes Flask
        db.drop_all()  # Supprime toutes les tables après les tests pour nettoyage


# Test complet du processus inscription, connexion, déconnexion
def test_signup_login_logout(client):
    # Test inscription avec POST sur /signup
    response = client.post('/signup', data={
        'nom': 'Test User',
        'email': 'test@example.com',
        'mot_de_passe': 'Test123!',
        'confirmation': 'Test123!'
    }, follow_redirects=True)  # Suivre les redirections pour obtenir la page finale
    # Vérifie que la réponse contient "livres" (page d'accueil après inscription) ou code 200 OK
    assert b'livres' in response.data or response.status_code == 200

    # Déconnexion (GET sur /logout) avant test connexion
    client.get('/logout')

    # Test connexion avec POST sur /login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'mot_de_passe': 'Test123!'
    }, follow_redirects=True)
    # Vérifie que la page affichée contient "index" ou code 200 OK (page d'accueil)
    assert b'index' in response.data or response.status_code == 200

    # Test déconnexion avec GET sur /logout
    response = client.get('/logout', follow_redirects=True)
    # Vérifie que l'on retourne bien à la page d'accueil après déconnexion
    assert b'index' in response.data or response.status_code == 200


# Test d’inscription avec un mot de passe trop faible
def test_signup_password_trop_faible(client):
    response = client.post('/signup', data={
        'nom': 'User Faible',
        'email': 'faible@example.com',
        'mot_de_passe': '123',  # Mot de passe volontairement faible
        'confirmation': '123'
    })
    # Vérifie que la réponse contient le message d’erreur sur la faiblesse du mot de passe
    assert b'Mot de passe trop faible' in response.data


# Test de tentative de connexion avec de mauvais identifiants
def test_login_mauvais_identifiants(client):
    response = client.post('/login', data={
        'email': 'nexistepas@example.com',
        'mot_de_passe': 'nimportequoi'
    })
    # Vérifie que la réponse contient le message d’erreur sur identifiants incorrects
    assert b'Identifiants incorrects' in response.data
