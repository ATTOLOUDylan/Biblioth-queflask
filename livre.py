import sqlite3

# ───── AJOUTER UN LIVRE ─────
def ajouter_livre():
    titre = input("Titre : ").strip()
    auteur = input("Auteur : ").strip()
    annee = input("Année : ").strip()
    quantite = int(input("Nombre d'exemplaires : "))

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO livres (titre, auteur, annee, exemplaires)
        VALUES (?, ?, ?, ?)
    """, (titre, auteur, annee, quantite))

    conn.commit()
    conn.close()
    print(f"✅ Livre '{titre}' ajouté avec succès ({quantite} exemplaires).")

# ───── LISTER LES LIVRES ─────
def lister_livres():
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("SELECT id, titre, auteur, annee, exemplaires FROM livres")
    livres = cur.fetchall()
    conn.close()

    if not livres:
        print("📭 Aucun livre disponible.")
    else:
        for l in livres:
            print(f"{l[0]}. {l[1]} - {l[2]} ({l[3]}) | Exemplaires : {l[4]}")

# ───── RECHERCHER UN LIVRE ─────
def rechercher_livre():
    mot = input("Mot-clé (titre ou auteur) : ").strip().lower()

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT id, titre, auteur, annee, exemplaires
        FROM livres
        WHERE LOWER(titre) LIKE ? OR LOWER(auteur) LIKE ?
    """, (f"%{mot}%", f"%{mot}%"))
    resultats = cur.fetchall()
    conn.close()

    if not resultats:
        print("❌ Aucun livre trouvé.")
    else:
        print("\n🔍 Résultats de la recherche :")
        for l in resultats:
            print(f"{l[0]}. {l[1]} - {l[2]} ({l[3]}) | Exemplaires : {l[4]}")

# ───── RENDRE UN LIVRE ─────
def rendre_livre(utilisateur_email):
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()

    # Récupérer les livres empruntés par l'utilisateur
    cur.execute("""
        SELECT e.id, l.titre
        FROM emprunts e
        JOIN livres l ON e.livre_id = l.id
        WHERE e.utilisateur_email = ?
    """, (utilisateur_email,))
    emprunts = cur.fetchall()

    if not emprunts:
        print("📭 Vous n'avez emprunté aucun livre.")
        conn.close()
        return

    print("\n📦 Vos livres empruntés :")
    for i, (emprunt_id, titre) in enumerate(emprunts, 1):
        print(f"{i}. {titre} (emprunt ID : {emprunt_id})")

    choix = input("Entrez le numéro du livre à rendre : ").strip()
    if not choix.isdigit() or int(choix) < 1 or int(choix) > len(emprunts):
        print("❌ Choix invalide.")
        conn.close()
        return

    emprunt_id, titre_rendu = emprunts[int(choix) - 1]

    # Récupérer l'ID du livre
    cur.execute("SELECT livre_id FROM emprunts WHERE id = ?", (emprunt_id,))
    livre = cur.fetchone()
    if not livre:
        print("❌ Erreur : emprunt non trouvé.")
        conn.close()
        return

    livre_id = livre[0]

    # Supprimer l’emprunt et rendre le livre
    cur.execute("DELETE FROM emprunts WHERE id = ?", (emprunt_id,))
    cur.execute("UPDATE livres SET exemplaires = exemplaires + 1 WHERE id = ?", (livre_id,))

    conn.commit()
    conn.close()
    print(f"✅ Livre '{titre_rendu}' rendu avec succès.")
