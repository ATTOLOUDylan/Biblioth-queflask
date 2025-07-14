from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.db import db, Utilisateur
import re

# Blueprint pour le profil utilisateur
profil_bp = Blueprint("profil_bp", __name__)

@profil_bp.route("/profil", methods=["GET", "POST"])
def profil():
    utilisateur = session.get("utilisateur")
    if not utilisateur:
        return redirect("/login")

    message = None

    # Récupère l'utilisateur connecté depuis la base
    user = Utilisateur.query.filter_by(email=utilisateur['email']).first()

    if request.method == 'POST':
        action = request.form.get("action")

        # --- Modifier l’email ---
        if action == "email":
            nouveau_email = request.form['nouveau_email'].strip().lower()

            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                # Vérifie si un autre utilisateur a déjà cet email
                if Utilisateur.query.filter_by(email=nouveau_email).first():
                    message = "❌ Cet email est déjà utilisé."
                else:
                    user.email = nouveau_email
                    db.session.commit()
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."
            else:
                message = "❌ Email invalide."

        # --- Modifier le mot de passe ---
        elif action == "pwd":
            ancien  = request.form['ancien']
            nouveau = request.form['nouveau']
            confirm = request.form['confirm']

            if user.mot_de_passe != ancien:
                message = "❌ Ancien mot de passe incorrect."
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                user.mot_de_passe = nouveau
                db.session.commit()
                message = "✅ Mot de passe modifié avec succès."

    return render_template("profil.html", utilisateur=utilisateur, message=message)
