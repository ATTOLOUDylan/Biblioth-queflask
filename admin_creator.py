# admin_creator.py

import sqlite3

def creer_admin():
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()

    # Supprimer un ancien admin s'il existe déjà
    cur.execute("DELETE FROM utilisateurs WHERE email = 'admin@gmail.com'")

    # Créer le nouvel admin
    cur.execute("""
        INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
        VALUES (?, ?, ?, ?)
    """, ("Admin", "admin@gmail.com", "admin2005", 1))

    conn.commit()
    conn.close()
    print("✅ Admin créé : admin@gmail.com / admin2005")

if __name__ == "__main__":
    creer_admin()
