# 📚 Projet Bibliothèque en Console

Une application Python simple pour gérer une petite bibliothèque en ligne de commande.  
Elle permet l’ajout de livres, la gestion des utilisateurs, et le suivi des emprunts, le tout **sans base de données** (stockage via fichiers JSON).

---

## 🚀 Fonctionnalités

- 📘 Ajouter un livre
- 📖 Lister tous les livres
- 🔍 Rechercher un livre par titre ou auteur
- 🧑 S’inscrire en tant qu’utilisateur
- 🔐 Se connecter
- 📥 Emprunter un livre
- 📤 Rendre un livre
- 💾 Sauvegarde automatique des données

---

## 📁 Structure du projet
```bash
bibliotheque/
├── bibliothèque.py # Menu principal de l'application
├── livre.py # Fonctions de gestion des livres
├── utilisateur.py # Fonctions pour gérer les utilisateurs
├── compte.py # Interface pour l'utilisateur connecté
├── livres.json # Fichier de stockage des livres
├── utilisateur.json # Fichier de stockage des utilisateurs
├── README.md # Ce fichier de documentation
```

---

## ▶️ Lancer le programme

Depuis un terminal :

```bash
python3 bibliothèque.py
---
```
## 🔧 Technologies utilisées

- Python 3.x
- Fichiers JSON (`livres.json`, `utilisateur.json`)
- Aucune bibliothèque externe

---

## 👤 Auteur

- **Dylan** – Développeur du projet

---

## 📜 Licence

Ce projet est libre de droits. Tu peux le copier, modifier et réutiliser à volonté.

