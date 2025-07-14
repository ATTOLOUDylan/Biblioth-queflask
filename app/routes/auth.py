from flask import Blueprint, render_template, request, redirect, session, url_for
from app import db
from app.models.db import Utilisateur
import re

auth_bp = Blueprint('auth', __name__)

# Fonction d'évaluation de mot de passe (inchangée)
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
    niveau_label = niveaux.get(niveau, "🟥 Faible")
    return niveau, niveau_label, remarques

@auth_bp.route('/')
def accueil():
    utilisateur = session.get("utilisateur")
    return render_template("index.html", utilisateur=utilisateur)

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

        if Utilisateur.query.filter_by(email=email).first():
            return render_template("signup.html", erreur="❌ Cet email est déjà inscrit.")
        if pwd != confirm:
            return render_template("signup.html", erreur="❌ Les mots de passe ne correspondent pas.")

        niveau, niveau_label, remarques = evaluer_mot_de_passe(pwd)
        if niveau < 3:
            return render_template(
                "signup.html",
                erreur="❌ Mot de passe trop faible.",
                niveau=niveau_label,
                remarques=remarques
            )

        nouvel_utilisateur = Utilisateur(nom=nom, email=email, mot_de_passe=pwd, is_admin=False)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        session['utilisateur'] = {'nom': nom, 'email': email, 'is_admin': False}
        return redirect(url_for('livres.livres'))

    return render_template("signup.html", niveau=None, remarques=[])

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        utilisateur = Utilisateur.query.filter_by(email=email, mot_de_passe=mot_de_passe).first()
        if utilisateur:
            session['utilisateur'] = {
                'nom': utilisateur.nom,
                'email': utilisateur.email,
                'is_admin': utilisateur.is_admin
            }
            return redirect(url_for('auth.accueil'))
        else:
            return render_template("login.html", erreur="❌ Identifiants incorrects")

    return render_template("login.html")

@auth_bp.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('auth.accueil'))
