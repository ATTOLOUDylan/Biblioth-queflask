from app import create_app, db
from app.models.db import Utilisateur, Livre, Emprunt

app = create_app()  # Création de l’application Flask avec la configuration

with app.app_context():
    # Crée toutes les tables en base si elles n'existent pas encore
    db.create_all()

if __name__ == "__main__":
    # Lance le serveur Flask en mode debug (rechargement automatique, messages d'erreur détaillés)
    app.run(debug=True)
