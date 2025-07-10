import mysql.connector

def creer_base():
    conn = mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

    cur = conn.cursor()

    # Table livres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titre VARCHAR(255) NOT NULL,
            auteur VARCHAR(255) NOT NULL,
            annee VARCHAR(4) NOT NULL,
            exemplaires INT DEFAULT 1
        )
    """)

    # Table utilisateurs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            is_admin TINYINT DEFAULT 0
        )
    """)

    # Table emprunts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emprunts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            utilisateur_email VARCHAR(255) NOT NULL,
            livre_id INT NOT NULL,
            date_emprunt DATETIME DEFAULT CURRENT_TIMESTAMP,
            date_limite DATE,
            FOREIGN KEY (utilisateur_email) REFERENCES utilisateurs(email),
            FOREIGN KEY (livre_id) REFERENCES livres(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données MySQL initialisée avec succès.")
