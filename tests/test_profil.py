from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.db import db, Utilisateur
import re

# Création du blueprint pour le profil utilisateur
profil_bp = Blueprint("profil_bp", __name__)

@profil_bp.route("/profil", methods=["GET", "POST"])
def profil():
    # Récupère les informations utilisateur stockées dans la session (connexion)
    utilisateur = session.get("utilisateur")
    # Si pas d'utilisateur connecté, redirige vers la page de connexion
    if not utilisateur:
        return redirect("/login")

    message = None  # Variable pour stocker les messages d'erreur ou succès

    # Recherche en base de données de l'utilisateur connecté via son email
    user = Utilisateur.query.filter_by(email=utilisateur['email']).first()

    # Si la requête est un POST (soumission formulaire)
    if request.method == 'POST':
        action = request.form.get("action")  # Quel formulaire a été soumis ? (email ou mot de passe)

        # --- Modifier l’email ---
        if action == "email":
            # Récupération et nettoyage du nouvel email depuis le formulaire
            nouveau_email = request.form['nouveau_email'].strip().lower()

            # Vérifie que le format de l'email est valide avec une expression régulière simple
            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                # Vérifie si un autre utilisateur a déjà cet email (pas de doublons)
                if Utilisateur.query.filter_by(email=nouveau_email).first():
                    message = "❌ Cet email est déjà utilisé."  # Message d'erreur si doublon
                else:
                    # Mise à jour du mail en base
                    user.email = nouveau_email
                    db.session.commit()  # Validation en base
                    # Met à jour aussi la session (sinon session garderait l'ancien email)
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."  # Message de succès
            else:
                # Email ne correspond pas au format attendu
                message = "❌ Email invalide."

        # --- Modifier le mot de passe ---
        elif action == "pwd":
            # Récupération des champs mot de passe depuis formulaire
            ancien  = request.form['ancien']
            nouveau = request.form['nouveau']
            confirm = request.form['confirm']

            # Vérifie que l'ancien mot de passe correspond à celui stocké en base
            if user.mot_de_passe != ancien:
                message = "❌ Ancien mot de passe incorrect."
            # Vérifie que le nouveau mot de passe correspond à la confirmation
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                # Mise à jour du mot de passe et sauvegarde en base
                user.mot_de_passe = nouveau
                db.session.commit()
                message = "✅ Mot de passe modifié avec succès."

    # Affiche la page profil avec l'utilisateur et un message éventuel
    return render_template("profil.html", utilisateur=utilisateur, message=message)
