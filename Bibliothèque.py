from livre import ajouter_livre, lister_livres, rechercher_livre
from utilisateur import ajouter_utilisateur, connexion_utilisateur, changer_mot_de_passe
from compte import compte
from db import creer_base

creer_base()

def menu():
    utilisateur_connecte = None

    while True:
        print("\n=== Menu Bibliothèque ===")

        if utilisateur_connecte:
            print(f"Connecté en tant que : {utilisateur_connecte['nom']} ({'Admin' if utilisateur_connecte['is_admin'] else 'Utilisateur'})")
            print("1. Lister les livres")
            print("2. Rechercher un livre")
            if utilisateur_connecte["is_admin"]:
                print("3. Ajouter un livre")
                print("4. Changer mot de passe")
                print("5. Accéder à mon compte")
                print("6. Se déconnecter")
            else:
                print("3. Changer mot de passe")
                print("4. Accéder à mon compte")
                print("5. Se déconnecter")

        else:
            print("1. Lister les livres")
            print("2. Rechercher un livre")
            print("3. S'inscrire")
            print("4. Se connecter")
            print("5. Quitter")

        choix = input("Votre choix : ").strip()

        if utilisateur_connecte:
            if choix == "1":
                lister_livres()
            elif choix == "2":
                rechercher_livre()
            elif utilisateur_connecte["is_admin"] and choix == "3":
                ajouter_livre()
            elif utilisateur_connecte["is_admin"] and choix == "4":
                changer_mot_de_passe()
            elif utilisateur_connecte["is_admin"] and choix == "5":
                compte(utilisateur_connecte)
            elif utilisateur_connecte["is_admin"] and choix == "6":
                utilisateur_connecte = None
                print("👋 Déconnecté.")
            elif not utilisateur_connecte["is_admin"] and choix == "3":
                changer_mot_de_passe()
            elif not utilisateur_connecte["is_admin"] and choix == "4":
                compte(utilisateur_connecte)
            elif not utilisateur_connecte["is_admin"] and choix == "5":
                utilisateur_connecte = None
                print("👋 Déconnecté.")
            else:
                print("❌ Choix invalide.")
        else:
            if choix == "1":
                lister_livres()
            elif choix == "2":
                rechercher_livre()
            elif choix == "3":
                ajouter_utilisateur()
            elif choix == "4":
                utilisateur_connecte = connexion_utilisateur()
            elif choix == "5":
                print("📦 À bientôt !")
                break
            else:
                print("❌ Choix invalide.")

if __name__ == "__main__":
    menu()
