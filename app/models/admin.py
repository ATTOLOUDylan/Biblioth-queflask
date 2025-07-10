import mysql.connector

def creer_admin():
    """
    Crée un compte admin SEULEMENT s'il n'en existe aucun (is_admin = 1).
    Peu importe son email ou mot de passe.
    """
    email_admin = "admin@gmail.com"
    mot_de_passe_admin = "admin2005"
    nom_admin = "Admin"

    conn = mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )
    cur = conn.cursor()

    # Vérifie s’il existe déjà un utilisateur admin
    cur.execute("SELECT id, email FROM utilisateurs WHERE is_admin = 1 LIMIT 1")
    admin_existant = cur.fetchone()

    if admin_existant:
        print(f"ℹ️ Un administrateur existe déjà (email : {admin_existant[1]})")
    else:
        cur.execute("""
            INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
            VALUES (%s, %s, %s, 1)
        """, (nom_admin, email_admin, mot_de_passe_admin))
        conn.commit()
        print(f"✅ Admin créé : {email_admin} / {mot_de_passe_admin}")

    conn.close()
