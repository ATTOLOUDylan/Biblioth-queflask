# 📚 Bibliothèque en ligne (Flask + MySQL)

Une application web simple de gestion de bibliothèque construite avec **Flask**, **MySQL**, **Bootstrap**, et le module d'envoi d’**emails** avec `smtplib`.  
Les utilisateurs peuvent s'inscrire, se connecter, emprunter et rendre des livres, et consulter leur profil.

---

## 🚀 Fonctionnalités

- 🔐 Authentification (inscription, connexion, déconnexion)
- 📚 Ajout, consultation, recherche et emprunt de livres
- 🗓️ Date limite d'emprunt automatique (7 jours)
- ✉️ Envoi d’un email de confirmation à l’utilisateur après chaque emprunt
- ⚙️ Espace **profil** pour modifier son email ou mot de passe
- 👤 Interface administrateur pour ajouter des livres
- ✅ Système de vérification de la force des mots de passe
- 📬 Stockage sécurisé des identifiants d’envoi email via fichier `.env`

---

## 🗂️ Structure du projet

bibliotheque/
├── app/
│ ├── init.py # Création de l'app Flask
│ ├── models/ # Fichiers liés à la base de données
│ │ ├── db.py # Création des tables MySQL
│ │ ├── admin.py # Création du compte admin
│ │ └── mail.py # Fonction d'envoi d'emails
│ ├── routes/ # Définition des routes (Blueprints)
│ │ ├── auth.py # Routes : login, signup, logout
│ │ ├── livres.py # Routes : livres, recherche, emprunter, rendre
│ │ └── profil.py # Route : profil utilisateur
│ ├── templates/ # Fichiers HTML (Jinja2)
│ └── static/ # Fichiers CSS, JS, images
├── run.py # Point d'entrée de l’application
├── .env # Variables d’environnement (non suivi par git)
├── .gitignore # Fichiers à ignorer par git
