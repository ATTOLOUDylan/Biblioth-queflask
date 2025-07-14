from flask import Blueprint, render_template, request, redirect, session, url_for
from app import db
from app.models.db import Utilisateur
import re

# Déclaration du blueprint d'authentification
auth_bp = Blueprint('auth', __name__)

# -----------------------------------------------
# Fonction d'évaluation de mot de passe
# Vérifie la complexité du mot de passe selon 5 critères :
# - Longueur >= 8
# - Lettres minuscules
# - Lettres majuscules
# - Chiffres
# - Caractères spéciaux
# Retourne :
#   - un score de 0 à 5
#   - un label de niveau (faible à excellent)
#   - des remarques sous forme de conseils
# -----------------------------------------------
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

# -----------------------------------------------
# Route : /
# Affiche la page d'accueil avec les informations
# de l'utilisateur connecté (si présent en session)
# -----------------------------------------------
@auth_bp.route('/')
def accueil():
    utilisateur = session.get("utilisateur")
    return render_template("index.html", utilisateur=utilisateur)

# -----------------------------------------------
# Route : /signup (GET et POST)
# Permet à un nouvel utilisateur de s'inscrire
# Étapes :
# - Vérifie les champs requis
# - Valide le format de l'email
# - Vérifie si l'email existe déjà
# - Compare les deux mots de passe
# - Évalue la qualité du mot de passe
# - Crée un nouvel utilisateur et le connecte
# - Redirige vers la liste des livres
# -----------------------------------------------
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

        # Vérification de l'unicité de l'email
        if Utilisateur.query.filter_by(email=email).first():
            return render_template("signup.html", erreur="❌ Cet email est déjà inscrit.")

        # Vérification de la confirmation du mot de passe
        if pwd != confirm:
            return render_template("signup.html", erreur="❌ Les mots de passe ne correspondent pas.")

        # Évaluation du mot de passe
        niveau, niveau_label, remarques = evaluer_mot_de_passe(pwd)
        if niveau < 3:
            return render_template(
                "signup.html",
                erreur="❌ Mot de passe trop faible.",
                niveau=niveau_label,
                remarques=remarques
            )

        # Création du nouvel utilisateur (⚠️ mot de passe stocké en clair)
        nouvel_utilisateur = Utilisateur(nom=nom, email=email, mot_de_passe=pwd, is_admin=False)
        db.session.add(nouvel_utilisateur)
        db.session.commit()

        # Enregistrement dans la session et redirection
        session['utilisateur'] = {'nom': nom, 'email': email, 'is_admin': False}
        return redirect(url_for('livres.livres'))

    # Si GET : affichage du formulaire
    return render_template("signup.html", niveau=None, remarques=[])

# -----------------------------------------------
# Route : /login (GET et POST)
# Permet à un utilisateur existant de se connecter
# Étapes :
# - Récupère les identifiants saisis
# - Vérifie leur correspondance avec la base
# - Si OK : stocke l'utilisateur dans la session
# - Sinon : affiche un message d’erreur
# -----------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        # Vérification des identifiants (⚠️ mot de passe non chiffré)
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

# -----------------------------------------------
# Route : /logout
# Déconnecte l'utilisateur en supprimant la session
# et redirige vers la page d'accueil
# -----------------------------------------------
@auth_bp.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('auth.accueil'))
