from flask import Blueprint, render_template, request, redirect, session, url_for
import mysql.connector
from datetime import datetime, timedelta
from app.models.mail import envoyer_email  # Module personnalisé pour l'envoi d'emails

# Déclaration du blueprint pour le groupe de routes liées aux livres
livres_bp = Blueprint('livres', __name__)

# Fonction pour se connecter à la base de données MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

# Page de liste des livres
@livres_bp.route('/livres')
def livres():
    utilisateur = session.get('utilisateur')  # Vérifie si un utilisateur est connecté

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, titre, auteur, annee, exemplaires FROM livres")
    livres = cur.fetchall()
    conn.close()

    return render_template("livres.html", livres=livres, utilisateur=utilisateur)

# Recherche de livres par titre ou auteur
@livres_bp.route('/recherche')
def recherche():
    utilisateur = session.get('utilisateur')
    q = request.args.get('q', '').strip().lower()  # Récupère la requête utilisateur

    livres_resultat = []
    if q:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, titre, auteur, annee, exemplaires
            FROM livres
            WHERE LOWER(titre) LIKE %s OR LOWER(auteur) LIKE %s
        """, (f'%{q}%', f'%{q}%'))
        livres_resultat = cur.fetchall()
        conn.close()

    return render_template("recherche.html", livres=livres_resultat, requete=q, utilisateur=utilisateur)

# Ajout d’un nouveau livre (réservé aux administrateurs)
@livres_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter_livre():
    utilisateur = session.get("utilisateur")
    if not utilisateur or not utilisateur.get("is_admin"):
        return redirect('/')  # Redirection si non-admin

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']
        exemplaires = request.form['exemplaires']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO livres (titre, auteur, annee, exemplaires)
            VALUES (%s, %s, %s, %s)
        """, (titre, auteur, annee, exemplaires))
        conn.commit()
        conn.close()
        return redirect('/livres')

    return render_template("ajouter.html")

# Emprunt d’un livre
@livres_bp.route('/emprunter/<int:livre_id>', methods=['POST'])
def emprunter(livre_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')  # Redirection vers la connexion

    conn = get_db()
    cur = conn.cursor()

    # Vérifie si le livre existe et récupère le titre
    cur.execute("SELECT titre FROM livres WHERE id = %s", (livre_id,))
    livre_info = cur.fetchone()
    if not livre_info:
        conn.close()
        return redirect('/livres')

    titre = livre_info[0]

    # Calcule la date limite d’emprunt (7 jours après la date actuelle)
    date_limite = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')

    # Enregistre l’emprunt dans la base de données
    cur.execute("""
        INSERT INTO emprunts (utilisateur_email, livre_id, date_limite)
        VALUES (%s, %s, %s)
    """, (utilisateur['email'], livre_id, date_limite))

    # Décrémente le nombre d’exemplaires disponibles
    cur.execute("UPDATE livres SET exemplaires = exemplaires - 1 WHERE id = %s", (livre_id,))
    conn.commit()
    conn.close()

    # Envoie d’un email de confirmation à l’utilisateur
    sujet = "📚 Confirmation d’emprunt de livre"
    contenu = f"""Bonjour {utilisateur['nom']},

Vous avez emprunté le livre : {titre}
📅 Date d'emprunt : {datetime.now().strftime('%Y-%m-%d')}
📆 Date limite de retour : {date_limite}

Merci de respecter cette date pour éviter une pénalité.

Cordialement,
La Bibliothèque
"""
    envoyer_email(utilisateur['email'], sujet, contenu)

    return redirect('/livres')

# Affiche les livres empruntés par l'utilisateur connecté
@livres_bp.route('/mes_emprunts')
def mes_emprunts():
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, l.titre, l.auteur, e.date_emprunt, e.date_limite
        FROM emprunts e
        JOIN livres l ON e.livre_id = l.id
        WHERE e.utilisateur_email = %s
    """, (utilisateur['email'],))
    emprunts = cur.fetchall()
    conn.close()

    return render_template("emprunter.html", emprunts=emprunts)

# Traitement du retour d’un livre
@livres_bp.route('/rendre/<int:emprunt_id>', methods=['POST'])
def rendre(emprunt_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    # Récupère l’ID du livre lié à l’emprunt
    cur.execute("SELECT livre_id FROM emprunts WHERE id = %s", (emprunt_id,))
    row = cur.fetchone()

    if row:
        livre_id = row[0]

        # Supprime l'emprunt
        cur.execute("DELETE FROM emprunts WHERE id = %s", (emprunt_id,))
        # Réaugmente le stock du livre
        cur.execute("UPDATE livres SET exemplaires = exemplaires + 1 WHERE id = %s", (livre_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('livres.mes_emprunts'))
