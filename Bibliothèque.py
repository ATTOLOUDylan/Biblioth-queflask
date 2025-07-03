import json
import os
from livre import charger_livres, sauvegarder_livres, ajouter_livre, lister_livres, rechercher_livre
from utilisateur import charger_util, sauvegarder_util, ajouter_util, connec_util
from compte import compte

def menu():
    livres = charger_livres()
    utilisateurs = charger_util()
    utilisateur_connecte = None

    while True:
        print("""
=== Menu Bibliothèque ===
1. Ajouter un livre
2. Lister les livres
3. Rechercher un livre
4. S'inscrire
5. Se connecter
6. Quitter
NB: Pour emprunter un livre, connectez-vous
""")
        choix = input("Votre choix : ")

        if choix == "1":
            ajouter_livre(livres)
            sauvegarder_livres(livres)

        elif choix == "2":
            lister_livres(livres)

        elif choix == "3":
            rechercher_livre(livres)

        elif choix == "4":
            ajouter_util(utilisateurs)
            sauvegarder_util(utilisateurs)
            print("Inscription réussie")

        elif choix == "5":
            utilisateur_connecte = connec_util(utilisateurs)
            if utilisateur_connecte:
                print(f"Bienvenue, {utilisateur_connecte['nom']} !")
                compte(utilisateur_connecte, utilisateurs, livres)
            else:
                print("Échec de la connexion.")

        elif choix == "6":
            sauvegarder_livres(livres)
            sauvegarder_util(utilisateurs)
            print("📦 Bibliothèque sauvegardée. Au revoir !")
            break

        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    menu()
