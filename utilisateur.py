import json
import os

FICHIER_UTIL = "utilisateur.json"

def charger_util():
    if os.path.exists(FICHIER_UTIL):
        with open(FICHIER_UTIL, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_util(util):
    with open(FICHIER_UTIL, "w", encoding="utf-8") as f:
        json.dump(util, f, indent=4, ensure_ascii=False)

def ajouter_util(util):
    nom = input("Nom utilisateur : ")
    email = input("Votre email : ")
    for user in util:
        if user["email"].lower() == email.lower():
            print("Cet email est déjà inscrit.")
            return
    pwd = input("Votre mot de passe : ")
    utils = {"nom": nom, "email": email, "pwd": pwd, "emprunts": []}
    util.append(utils)
    print(f"Utilisateur '{nom}' ajouté.")

def connec_util(utilisateurs):
    nom = input("Nom utilisateur : ").lower()
    pwd = input("Mot de passe : ").lower()

    for user in utilisateurs:
        if user["nom"].lower() == nom and user["pwd"].lower() == pwd:
            return user
    print("Utilisateur ou mot de passe incorrect.")
    return None

def emprunter_livre(utilisateurs, livres, utilisateur_connecte):
    livres_disponibles = [l for l in livres if l["disponible"]]
    if not livres_disponibles:
        print("Aucun livre disponible actuellement.")
        return

    print("\nLivres disponibles :")
    for i, livre in enumerate(livres_disponibles, 1):
        print(f"{i}. {livre['titre']} - {livre['auteur']}")

    titre_choisi = input("Titre du livre à emprunter : ")

    for livre in livres:
        if livre["titre"].lower() == titre_choisi.lower():
            if not livre["disponible"]:
                print("Ce livre est déjà emprunté.")
                return
            utilisateur_connecte["emprunts"].append(livre["titre"])
            livre["disponible"] = False
            print(f"Livre '{livre['titre']}' emprunté avec succès.")
            return

    print("Livre introuvable.")
