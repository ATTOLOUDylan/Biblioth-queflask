import mysql.connector

# Fonction pour créer un compte administrateur si aucun n'existe
# Basé sur le flag 'is_admin' dans la table utilisateurs

def creer_admin():
    """
    Crée un compte admin SEULEMENT s'il n'en existe aucun (is_admin = 1).
    Peu importe son email ou mot de passe.
    """
    # Informations par défaut pour l'administrateur
    email_admin = "admin@gmail.com"
    mot_de_passe_admin = "admin2005"
    nom_admin = "Admin"

    # Connexion à la base MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )
    cur = conn.cursor()

    # Vérifier s'il existe déjà un utilisateur avec is_admin = 1
    cur.execute("SELECT id, email FROM utilisateurs WHERE is_admin = 1 LIMIT 1")
    admin_existant = cur.fetchone()

    # Si un admin existe, ne rien faire (évite doublon)
    if admin_existant:
        print(f"ℹ️ Un administrateur existe déjà (email : {admin_existant[1]})")
    else:
        # Sinon, insérer le nouvel admin avec le flag is_admin à 1
        cur.execute(
            """
            INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
            VALUES (%s, %s, %s, 1)
            """,
            (nom_admin, email_admin, mot_de_passe_admin)
        )
        conn.commit()
        print(f"✅ Admin créé : {email_admin} / {mot_de_passe_admin}")

    # Fermer la connexion
    conn.close()
