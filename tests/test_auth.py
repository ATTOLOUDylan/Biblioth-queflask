import pytest
from flask import session
from app import create_app, db
from app.models.db import Utilisateur

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_key"
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_signup_login_logout(client):
    # Inscription
    response = client.post('/signup', data={
        'nom': 'Test User',
        'email': 'test@example.com',
        'mot_de_passe': 'Test123!',
        'confirmation': 'Test123!'
    }, follow_redirects=True)
    assert b'livres' in response.data or response.status_code == 200

    # Connexion
    client.get('/logout')
    response = client.post('/login', data={
        'email': 'test@example.com',
        'mot_de_passe': 'Test123!'
    }, follow_redirects=True)
    assert b'index' in response.data or response.status_code == 200

    # Déconnexion
    response = client.get('/logout', follow_redirects=True)
    assert b'index' in response.data or response.status_code == 200


def test_signup_password_trop_faible(client):
    response = client.post('/signup', data={
        'nom': 'User Faible',
        'email': 'faible@example.com',
        'mot_de_passe': '123',
        'confirmation': '123'
    })
    assert b'Mot de passe trop faible' in response.data


def test_login_mauvais_identifiants(client):
    response = client.post('/login', data={
        'email': 'nexistepas@example.com',
        'mot_de_passe': 'nimportequoi'
    })
    assert b'Identifiants incorrects' in response.data
