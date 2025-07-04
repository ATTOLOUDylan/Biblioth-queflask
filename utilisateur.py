import json
import os
from getpass import getpass

FICHIER_UTIL = "utilisateur.json"

def charger_util():
    if os.path.exists(FICHIER_UTIL):
        with open(FICHIER_UTIL, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_util(util):
    with open(FICHIER_UTIL, "w", encoding="utf-8") as f:
        json.dump(util, f, indent=4, ensure_ascii=False)

def email_valide(email):
    """Vérifie si l'email est valide avec des règles simples."""
    if "@" not in email or "." not in email:
        return False
    if email.count("@") != 1:
        return False
    nom, domaine = email.split("@")
    if not nom or not domaine:
        return False
    if "." not in domaine:
        return False
    if domaine.startswith(".") or domaine.endswith("."):
        return False
    return True

import re

def evaluer_mot_de_passe(pwd):
    niveau = 0
    remarques = []

    if len(pwd) >= 8:
        niveau += 1
    else:
        remarques.append("🔸 Mot de passe trop court (minimum 8 caractères)")

    if re.search(r"[a-z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres minuscules")

    if re.search(r"[A-Z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres majuscules")

    if re.search(r"[0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des chiffres")

    if re.search(r"[^a-zA-Z0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter un caractère spécial (ex: @, #, !, ?)")

    niveaux = {
        1: "🟥 Faible",
        2: "🟧 Moyen",
        3: "🟨 Acceptable",
        4: "🟩 Bon",
        5: "🟦 Excellent"
    }

    print(f"\n🔐 Niveau de sécurité du mot de passe : {niveaux[niveau]}")
    for r in remarques:
        print(r)
    
    return niveau

def ajouter_util(util):
    nom = input("Nom utilisateur : ")
    email = input("Votre email : ")

    if not email_valide(email):
        print("❌ Email invalide.")
        return

    for user in util:
        if user["email"].lower() == email.lower():
            print("Cet email est déjà inscrit.")
            return

    pwd = getpass("Votre mot de passe : ")
    niveau = evaluer_mot_de_passe(pwd)

    if niveau < 3:
        print("❗️Mot de passe trop faible. Veuillez en choisir un plus sécurisé.")
        return

    pwd2 = getpass("Confirmer votre mot de passe : ")
    if pwd != pwd2:
        print("❌ Les mots de passe ne correspondent pas.")
        return

    utils = {"nom": nom, "email": email, "pwd": pwd, "emprunts": []}
    util.append(utils)
    print(f"✅ Utilisateur '{nom}' ajouté avec succès.")


def connec_util(utilisateurs):
    nom = input("Nom utilisateur : ").lower()
    pwd = input("Mot de passe : ").lower()

    for user in utilisateurs:
        if user["nom"].lower() == nom and user["pwd"].lower() == pwd:
            return user
    print("Utilisateur ou mot de passe incorrect.")
    return None

def changer_mot_de_passe(utilisateurs):
    email = input("Entrez votre email : ").strip().lower()
    ancien_mdp = input("Entrez votre ancien mot de passe : ").strip()
    
    # Trouver l'utilisateur par email
    utilisateur = None
    for u in utilisateurs:
        if u["email"].lower() == email:
            utilisateur = u
            break
    
    if not utilisateur:
        print("❌ Utilisateur non trouvé.")
        return
    
    if utilisateur["pwd"] != ancien_mdp:
        print("❌ Ancien mot de passe incorrect.")
        return
    
    nouveau_mdp = getpass("Entrez votre nouveau mot de passe : ").strip()
    niveau = evaluer_mot_de_passe(nouveau_mdp)

    if niveau < 3:
        print("❗️Mot de passe trop faible. Veuillez en choisir un plus sécurisé.")
        return
    
    confirmation = getpass("Confirmez votre nouveau mot de passe : ").strip()
    
    if nouveau_mdp != confirmation:
        print("❌ Les mots de passe ne correspondent pas.")
        return
    
    utilisateur["pwd"] = nouveau_mdp
    print("✅ Mot de passe modifié avec succès.")

def emprunter_livre(utilisateurs, livres, utilisateur_connecte):
    livres_disponibles = [l for l in livres if l.get("quantite", 0) > 0]

    if not livres_disponibles:
        print("📭 Aucun livre disponible actuellement.")
        return

    print("\n📚 Livres disponibles :")
    for i, livre in enumerate(livres_disponibles, 1):
        print(f"{i}. {livre['titre']} - {livre['auteur']} (Exemplaires : {livre['quantite']})")

    choix = input("Entrez le **numéro** ou le **titre** du livre à emprunter : ").strip()

    livre_choisi = None

    # 📌 Vérifie si le choix est un numéro (ID)
    if choix.isdigit():
        index = int(choix) - 1
        if 0 <= index < len(livres_disponibles):
            livre_choisi = livres_disponibles[index]
    else:
        # 📌 Sinon on cherche par titre
        for livre in livres_disponibles:
            if livre["titre"].lower() == choix.lower():
                livre_choisi = livre
                break

    if not livre_choisi:
        print("❌ Livre introuvable ou plus disponible.")
        return

    # Ajoute le livre à l'utilisateur
    utilisateur_connecte["emprunts"].append(livre_choisi["titre"])
    livre_choisi["quantite"] -= 1
    print(f"✅ Livre '{livre_choisi['titre']}' emprunté avec succès.")


