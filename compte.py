from utilisateur import emprunter_livre
from livre import rendre_livre, lister_livres
from utilisateur import sauvegarder_util
from livre import sauvegarder_livres

def compte(user, utilisateurs, livres):
    while True:
        print(f"""
--- Menu Utilisateur : {user['nom']} ---
1. Emprunter un livre
2. Lister les livres empruntés
3. Rendre un livre
4. Se déconnecter
""")
        choix = input("Votre choix : ")
        if choix == "1":
            emprunter_livre(utilisateurs, livres, user)
            sauvegarder_util(utilisateurs)
            sauvegarder_livres(livres)
        elif choix == "2":
            if user["emprunts"]:
                print("\nVos livres empruntés :")
                for livre in user["emprunts"]:
                    print(f"- {livre}")
            else:
                print("Vous n'avez emprunté aucun livre.")
        elif choix == "3":
            rendre_livre(utilisateurs, livres, user)
            sauvegarder_util(utilisateurs)
            sauvegarder_livres(livres)
        elif choix == "4":
            print("Déconnexion. Au revoir !")
            break
        else:
            print("Choix invalide.")
