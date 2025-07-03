import json
import os

FICHIER_LIVRES = "livres.json"

def charger_livres():
    if os.path.exists(FICHIER_LIVRES):
        with open(FICHIER_LIVRES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_livres(livres):
    with open(FICHIER_LIVRES, "w", encoding="utf-8") as f:
        json.dump(livres, f, indent=4, ensure_ascii=False)

def ajouter_livre(livres):
    titre = input("Titre du livre : ").strip()
    auteur = input("Auteur : ").strip()
    annee = input("Année de publication : ").strip()
    livre = {"titre": titre, "auteur": auteur, "année": annee, "disponible": True}
    livres.append(livre)
    print(f"Livre '{titre}' ajouté.")

def lister_livres(livres):
    if not livres:
        print("Aucun livre dans la bibliothèque.")
        return
    print("\nListe des livres :")
    for i, livre in enumerate(livres, 1):
        dispo = "Oui" if livre["disponible"] else "Non"
        print(f"{i}. {livre['titre']} - {livre['auteur']} ({livre['année']}) | Disponible : {dispo}")

def rechercher_livre(livres):
    mot = input("Mot-clé (titre ou auteur) : ").strip().lower()
    resultats = [l for l in livres if mot in l["titre"].lower() or mot in l["auteur"].lower()]
    if not resultats:
        print("Aucun livre trouvé.")
    else:
        print("\nRésultats de la recherche :")
        for livre in resultats:
            dispo = "Oui" if livre["disponible"] else "Non"
            print(f"- {livre['titre']} - {livre['auteur']} ({livre['année']}) | Disponible : {dispo}")

def rendre_livre(utilisateurs, livres, utilisateur_connecte):
    if not utilisateur_connecte["emprunts"]:
        print("Vous n'avez aucun livre emprunté.")
        return

    print("\nVos livres empruntés :")
    for i, titre in enumerate(utilisateur_connecte["emprunts"], 1):
        print(f"{i}. {titre}")

    choix = input("Titre du livre à rendre : ")

    if choix in utilisateur_connecte["emprunts"]:
        utilisateur_connecte["emprunts"].remove(choix)
        for livre in livres:
            if livre["titre"].lower() == choix.lower():
                livre["disponible"] = True
                print(f"Livre '{livre['titre']}' rendu avec succès.")
                return
    else:
        print("Ce livre n'est pas dans votre liste d'emprunts.")
