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
```plaintext
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
```


---

## 🛠️ Installation

1. **Cloner le projet** :

```bash
git clone https://github.com/ATTOLOUDylan/Biblioth-queflask.git
cd Bibliotheque
```
2.**Créer un environnement virtuel** :
```bash
python3 -m venv venv
source venv/bin/activate
```
3.**Installer les dépendances** :
```bash
pip install -r requirements.txt

```
4.**Configurer le fichier .env** :

Crée un fichier .env à la racine avec ce contenu :
```bash
MAIL_USER=ton_email@gmail.com
MAIL_PASSWORD=ton_mot_de_passe_application
```
> 🔐 **Important :** Utilise un **mot de passe d’application Gmail** (ne jamais utiliser ton mot de passe personnel Gmail).  
> 👉 [Voir comment créer un mot de passe d’application](https://support.google.com/accounts/answer/185833?hl=fr)

5.**Lancer l'application** :
```bash
python run.py
```
Puis ouvrir http://127.0.0.1:5000 dans un navigateur.

---
✅ **Compte admin par défaut**

| Email             | Mot de passe |
|-------------------|--------------|
| admin@gmail.com   | admin2005    |

> Il est créé automatiquement au premier lancement s’il n’existe pas.

---
📄 **Licence**

Ce projet est open-source et publié sous une licence.  
➡️ Consulte le fichier [`LICENCE`](LICENCE) pour plus de détails.
