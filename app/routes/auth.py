from flask import Blueprint, render_template, request, redirect, session, url_for
import mysql.connector
import re

# Blueprint pour l'authentification (inscription, connexion, déconnexion)
auth_bp = Blueprint('auth', __name__)

# Fonction utilitaire pour obtenir une connexion à la base MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

# Fonction pour évaluer la robustesse d'un mot de passe
def evaluer_mot_de_passe(pwd):
    niveau = 0
    remarques = []

    # Critère longueur minimale
    if len(pwd) >= 8:
        niveau += 1
    else:
        remarques.append("🔸 Mot de passe trop court (minimum 8 caractères)")

    # Critère lettre minuscule
    if re.search(r"[a-z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres minuscules")

    # Critère lettre majuscule
    if re.search(r"[A-Z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres majuscules")

    # Critère chiffre
    if re.search(r"[0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des chiffres")

    # Critère caractère spécial
    if re.search(r"[^a-zA-Z0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter un caractère spécial (ex: @, #, !, ?)")

    # Labels pour chaque niveau de robustesse
    niveaux = {
        1: "🟥 Faible",
        2: "🟧 Moyen",
        3: "🟨 Acceptable",
        4: "🟩 Bon",
        5: "🟦 Excellent"
    }
    niveau_label = niveaux.get(niveau, "🟥 Faible")
    return niveau, niveau_label, remarques

# Route d'accueil: redirige vers la page principale (index.html)
@auth_bp.route('/')
def accueil():
    utilisateur = session.get("utilisateur")
    return render_template("index.html", utilisateur=utilisateur)

# Route d'inscription (signup)
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nom = request.form['nom'].strip()
        email = request.form['email'].strip().lower()
        pwd = request.form['mot_de_passe']
        confirm = request.form.get('confirmation', '').strip()

        # Vérification des champs obligatoires
        if not nom or not email or not pwd:
            return render_template("signup.html", erreur="❌ Tous les champs sont obligatoires.")
        # Vérification du format de l'email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("signup.html", erreur="❌ Email invalide.")

        # Connexion DB pour vérifier l'existence de l'email
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
        exist = cur.fetchone()
        if exist:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà inscrit.")

        # Vérification de la confirmation du mot de passe
        if pwd != confirm:
            conn.close()
            return render_template("signup.html", erreur="❌ Les mots de passe ne correspondent pas.")

        # Évaluation de la robustesse du mot de passe
        niveau, niveau_label, remarques = evaluer_mot_de_passe(pwd)
        if niveau < 3:
            conn.close()
            return render_template(
                "signup.html",
                erreur="❌ Mot de passe trop faible.",
                niveau=niveau_label,
                remarques=remarques
            )

        # Insertion de l'utilisateur dans la base
        try:
            cur.execute(
                """
                INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
                VALUES (%s, %s, %s, 0)
                """,
                (nom, email, pwd)
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà utilisé.")
        conn.close()

        # Création de la session utilisateur
        session['utilisateur'] = {'nom': nom, 'email': email, 'is_admin': False}
        # Redirection vers la liste des livres
        return redirect(url_for('livres.livres'))

    # Méthode GET: affiche simplement le formulaire
    return render_template("signup.html", niveau=None, remarques=[])

# Route de connexion (login)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT nom, email, is_admin FROM utilisateurs WHERE email=%s AND mot_de_passe=%s",
            (email, mot_de_passe)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            # Stocke les infos essentielles en session
            session['utilisateur'] = {
                'nom': user[0],
                'email': user[1],
                'is_admin': bool(user[2])
            }
            return redirect(url_for('auth.accueil'))
        else:
            return render_template("login.html", erreur="❌ Identifiants incorrects")

    # Méthode GET: affiche le formulaire de connexion
    return render_template("login.html")

# Route de déconnexion (logout)
@auth_bp.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('auth.accueil'))
