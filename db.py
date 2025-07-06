import sqlite3

def creer_base():
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()

    # Table livres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            annee TEXT NOT NULL,
            exemplaires INTEGER DEFAULT 1
        )
    """)

    # Table utilisateurs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    """)

    # Table emprunts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_email TEXT NOT NULL,
            livre_id INTEGER NOT NULL,
            date_emprunt TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (utilisateur_email) REFERENCES utilisateurs(email),
            FOREIGN KEY (livre_id) REFERENCES livres(id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec succès.")
