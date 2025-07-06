import sqlite3
import re
from getpass import getpass

# ───── VALIDATION EMAIL ─────
def email_valide(email):
    if "@" not in email or "." not in email:
        return False
    if email.count("@") != 1:
        return False
    nom, domaine = email.split("@")
    if not nom or not domaine:
        return False
    if "." not in domaine:
        return False
    if domaine.startswith(".") or domaine.endswith("."):
        return False
    return True

# ───── EVALUATION MOT DE PASSE ─────
def evaluer_mot_de_passe(pwd):
    niveau = 0
    remarques = []

    if len(pwd) >= 8: niveau += 1
    else: remarques.append("🔸 Mot de passe trop court (minimum 8 caractères)")

    if re.search(r"[a-z]", pwd): niveau += 1
    else: remarques.append("🔸 Ajouter des lettres minuscules")

    if re.search(r"[A-Z]", pwd): niveau += 1
    else: remarques.append("🔸 Ajouter des lettres majuscules")

    if re.search(r"[0-9]", pwd): niveau += 1
    else: remarques.append("🔸 Ajouter des chiffres")

    if re.search(r"[^a-zA-Z0-9]", pwd): niveau += 1
    else: remarques.append("🔸 Ajouter un caractère spécial (ex: @, #, !, ?)")

    niveaux = {
        1: "🟥 Faible",
        2: "🟧 Moyen",
        3: "🟨 Acceptable",
        4: "🟩 Bon",
        5: "🟦 Excellent"
    }

    print(f"\n🔐 Niveau de sécurité du mot de passe : {niveaux[niveau]}")
    for r in remarques:
        print(r)

    return niveau

# ───── INSCRIPTION UTILISATEUR ─────
def ajouter_utilisateur():
    nom = input("Nom utilisateur : ").strip()
    email = input("Votre email : ").strip()

    if not email_valide(email):
        print("❌ Email invalide.")
        return

    pwd = getpass("Votre mot de passe : ")
    niveau = evaluer_mot_de_passe(pwd)

    if niveau < 3:
        print("❗️Mot de passe trop faible.")
        return

    pwd2 = getpass("Confirmer votre mot de passe : ")
    if pwd != pwd2:
        print("❌ Les mots de passe ne correspondent pas.")
        return

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    try:
        cur.execute("""
          INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
          VALUES (?, ?, ?, 0)
          """, (nom, email, pwd))
        conn.commit()
        print(f"✅ Utilisateur '{nom}' ajouté avec succès.")
    except sqlite3.IntegrityError:
        print("❌ Cet email est déjà inscrit.")
    conn.close()

# ───── CONNEXION UTILISATEUR ─────
def connexion_utilisateur():
    email = input("Email : ").strip().lower()
    mot_de_passe = getpass("Mot de passe : ").strip()

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT nom, email, is_admin 
        FROM utilisateurs 
        WHERE email = ? AND mot_de_passe = ?
    """, (email, mot_de_passe))
    user = cur.fetchone()
    conn.close()

    if user:
        print(f"✅ Connexion réussie. Bienvenue {user[0]} !")
        return {
            "nom": user[0],
            "email": user[1],
            "is_admin": bool(user[2])  # <= Très important !
        }
    else:
        print("❌ Email ou mot de passe incorrect.")
        return None


# ───── CHANGER MOT DE PASSE ─────
def changer_mot_de_passe():
    email = input("Entrez votre email : ").strip().lower()
    ancien_mdp = getpass("Entrez votre ancien mot de passe : ").strip()

    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()
    cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = ?", (email,))
    user = cur.fetchone()

    if not user:
        print("❌ Utilisateur non trouvé.")
        conn.close()
        return

    if user[0] != ancien_mdp:
        print("❌ Ancien mot de passe incorrect.")
        conn.close()
        return

    nouveau_mdp = getpass("Entrez votre nouveau mot de passe : ").strip()
    niveau = evaluer_mot_de_passe(nouveau_mdp)

    if niveau < 3:
        print("❗️Mot de passe trop faible.")
        conn.close()
        return

    confirmation = getpass("Confirmez votre nouveau mot de passe : ").strip()

    if nouveau_mdp != confirmation:
        print("❌ Les mots de passe ne correspondent pas.")
        conn.close()
        return

    cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE email = ?", (nouveau_mdp, email))
    conn.commit()
    conn.close()
    print("✅ Mot de passe modifié avec succès.")
def emprunter_livre(utilisateur_email):
    conn = sqlite3.connect("bibliotheque.db")
    cur = conn.cursor()

    # Liste des livres disponibles
    cur.execute("SELECT id, titre, auteur, exemplaires FROM livres WHERE exemplaires > 0")
    livres = cur.fetchall()

    if not livres:
        print("📭 Aucun livre disponible.")
        conn.close()
        return

    print("\n📚 Livres disponibles :")
    for livre in livres:
        print(f"{livre[0]}. {livre[1]} - {livre[2]} | Exemplaires : {livre[3]}")

    choix = input("Entrez l'ID du livre à emprunter : ").strip()
    if not choix.isdigit():
        print("❌ Entrée invalide.")
        conn.close()
        return

    livre_id = int(choix)

    # Vérifier si le livre existe et a des exemplaires
    cur.execute("SELECT exemplaires FROM livres WHERE id = ?", (livre_id,))
    result = cur.fetchone()

    if not result:
        print("❌ Livre introuvable.")
        conn.close()
        return
    elif result[0] <= 0:
        print("❌ Aucun exemplaire disponible.")
        conn.close()
        return

    # Enregistrer l'emprunt
    cur.execute("""
        INSERT INTO emprunts (utilisateur_email, livre_id)
        VALUES (?, ?)
    """, (utilisateur_email, livre_id))

    # Mettre à jour la table livres
    cur.execute("""
        UPDATE livres SET exemplaires = exemplaires - 1 WHERE id = ?
    """, (livre_id,))

    conn.commit()
    conn.close()
    print("✅ Livre emprunté avec succès.")




