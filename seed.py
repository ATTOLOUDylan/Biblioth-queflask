from app import create_app, db
from app.models.db import Utilisateur, Livre, Emprunt
from datetime import datetime, timedelta

app = create_app()  # Création de l'application Flask

with app.app_context():  # Context d’application pour accéder à la base

    db.drop_all()      # Supprime toutes les tables (réinitialisation)
    db.create_all()    # Crée toutes les tables selon les modèles SQLAlchemy

    # ----- Création des utilisateurs -----
    user1 = Utilisateur(nom="Alice", email="alice@example.com", mot_de_passe="alice123", is_admin=False)
    user2 = Utilisateur(nom="Bob", email="bob@example.com", mot_de_passe="bob123", is_admin=False)
    db.session.add_all([user1, user2])  # Ajoute les utilisateurs à la session

    # ----- Création des livres -----
    livre1 = Livre(titre="1984", auteur="George Orwell", annee="1949", exemplaires=2)
    livre2 = Livre(titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry", annee="1943", exemplaires=3)
    livre3 = Livre(titre="Harry Potter à l'école des sorciers", auteur="J.K. Rowling", annee="1997", exemplaires=1)
    db.session.add_all([livre1, livre2, livre3])  # Ajoute les livres à la session

    db.session.commit()  # ⚠️ Validation en base avant d’insérer les emprunts

    # ----- Création des emprunts -----
    emprunt1 = Emprunt(
        utilisateur_email="alice@example.com",
        livre_id=livre1.id,
        date_emprunt=datetime.utcnow(),
        date_limite=(datetime.utcnow() + timedelta(days=14)).date()  # 14 jours pour rendre le livre
    )
    emprunt2 = Emprunt(
        utilisateur_email="bob@example.com",
        livre_id=livre2.id,
        date_emprunt=datetime.utcnow(),
        date_limite=(datetime.utcnow() + timedelta(days=7)).date()   # 7 jours pour rendre le livre
    )

    db.session.add_all([emprunt1, emprunt2])  # Ajoute les emprunts à la session
    db.session.commit()  # Validation finale en base

    print("✅ Données de test insérées (utilisateurs, livres, emprunts)")
