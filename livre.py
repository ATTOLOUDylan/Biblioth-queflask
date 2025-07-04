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
    nom = input("Nom utilisateur : ").lower()
    pwd = input("Mot de passe : ").lower()

    if nom == "admin" and pwd == "admin2005":
        titre = input("Titre du livre : ").strip()
        auteur = input("Auteur : ").strip()
        annee = input("Année de publication : ").strip()
        quantite = int(input("Nombre d'exemplaires : ").strip())

        livre = {
            "titre": titre,
            "auteur": auteur,
            "année": annee,
            "quantite": quantite
        }

        livres.append(livre)
        print(f"Livre '{titre}' ajouté ({quantite} exemplaires).")
    else:
        print("❌ Accès refusé.")


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
    emprunts = utilisateur_connecte.get("emprunts", [])

    if not emprunts:
        print("📭 Vous n'avez emprunté aucun livre.")
        return

    print("\n📦 Vos livres empruntés :")
    for i, titre in enumerate(emprunts, 1):
        print(f"{i}. {titre}")

    choix = input("Entrez le **numéro** ou le **titre** du livre à rendre : ").strip()

    titre_rendu = None

    # Si l'utilisateur donne un numéro
    if choix.isdigit():
        index = int(choix) - 1
        if 0 <= index < len(emprunts):
            titre_rendu = emprunts[index]
    else:
        # Sinon, il tape le titre
        for t in emprunts:
            if t.lower() == choix.lower():
                titre_rendu = t
                break

    if not titre_rendu:
        print("❌ Livre non trouvé dans vos emprunts.")
        return

    # Retirer le titre de la liste d'emprunts
    utilisateur_connecte["emprunts"].remove(titre_rendu)

    # Augmenter la quantité disponible dans livres.json
    for livre in livres:
        if livre["titre"].lower() == titre_rendu.lower():
            livre["quantite"] = livre.get("quantite", 0) + 1
            print(f"✅ Livre '{titre_rendu}' rendu avec succès.")
            return

    print("⚠️ Erreur : Livre non trouvé dans la bibliothèque.")

