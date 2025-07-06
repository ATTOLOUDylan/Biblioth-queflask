from utilisateur import emprunter_livre
from livre import rendre_livre

import sqlite3

def compte(utilisateur_connecte):
    email = utilisateur_connecte["email"]

    while True:
        print(f"""
--- Menu Utilisateur : {utilisateur_connecte['nom']} ---
1. Emprunter un livre
2. Lister mes emprunts
3. Rendre un livre
4. Se déconnecter
""")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            emprunter_livre(email)

        elif choix == "2":
            # Afficher les livres empruntés depuis la base
            conn = sqlite3.connect("bibliotheque.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT l.titre, l.auteur
                FROM emprunts e
                JOIN livres l ON e.livre_id = l.id
                WHERE e.utilisateur_email = ?
            """, (email,))
            emprunts = cur.fetchall()
            conn.close()

            if not emprunts:
                print("📭 Vous n'avez emprunté aucun livre.")
            else:
                print("\n📘 Vos livres empruntés :")
                for titre, auteur in emprunts:
                    print(f"- {titre} ({auteur})")

        elif choix == "3":
            rendre_livre(email)

        elif choix == "4":
            print("👋 Déconnexion réussie.")
            break

        else:
            print("❌ Choix invalide.")
