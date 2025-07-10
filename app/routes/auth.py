from flask import Blueprint, render_template, request, redirect, session, url_for
import mysql.connector
import re

auth_bp = Blueprint('auth', __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

@auth_bp.route('/')
def accueil():
    utilisateur = session.get("utilisateur")
    return render_template("index.html", utilisateur=utilisateur)
    
def evaluer_mot_de_passe(pwd):
    niveau = 0
    remarques = []

    if len(pwd) >= 8:
        niveau += 1
    else:
        remarques.append("🔸 Mot de passe trop court (minimum 8 caractères)")

    if re.search(r"[a-z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres minuscules")

    if re.search(r"[A-Z]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des lettres majuscules")

    if re.search(r"[0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter des chiffres")

    if re.search(r"[^a-zA-Z0-9]", pwd):
        niveau += 1
    else:
        remarques.append("🔸 Ajouter un caractère spécial (ex: @, #, !, ?)")

    niveaux = {
        1: "🟥 Faible",
        2: "🟧 Moyen",
        3: "🟨 Acceptable",
        4: "🟩 Bon",
        5: "🟦 Excellent"
    }

    niveau_label = niveaux[niveau]
    return niveau, niveau_label, remarques

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nom = request.form['nom'].strip()
        email = request.form['email'].strip().lower()
        pwd = request.form['mot_de_passe']
        confirm = request.form.get('confirmation', '').strip()

        if not nom or not email or not pwd:
            return render_template("signup.html", erreur="❌ Tous les champs sont obligatoires.")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("signup.html", erreur="❌ Email invalide.")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM utilisateurs WHERE email = %s", (email,))
        exist = cur.fetchone()
        if exist:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà inscrit.")

        if pwd != confirm:
            return render_template("signup.html", erreur="❌ Les mots de passe ne correspondent pas.")

        niveau, niveau_label, remarques = evaluer_mot_de_passe(pwd)
        if niveau < 3:
            return render_template("signup.html", erreur="❌ Mot de passe trop faible.", niveau=niveau_label, remarques=remarques)

        try:
            cur.execute("""
                INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
                VALUES (%s, %s, %s, 0)
            """, (nom, email, pwd))
            conn.commit()
        except mysql.connector.IntegrityError:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà utilisé.")
        conn.close()

        session['utilisateur'] = {'nom': nom, 'email': email, 'is_admin': False}
        return redirect(url_for('livres.livres'))

    return render_template("signup.html", niveau=None, remarques=[])

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT nom, email, is_admin FROM utilisateurs WHERE email=%s AND mot_de_passe=%s", (email, mot_de_passe))
        user = cur.fetchone()
        conn.close()

        if user:
            session['utilisateur'] = {
                'nom': user[0],
                'email': user[1],
                'is_admin': bool(user[2])
            }
            return redirect(url_for('accueil'))
        else:
            return render_template("login.html", erreur="❌ Identifiants incorrects")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect('/')
