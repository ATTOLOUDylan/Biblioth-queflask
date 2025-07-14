from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.db import db, Utilisateur
import re

# --------------------------------------------------------
# Déclaration du blueprint pour les routes liées au profil
# --------------------------------------------------------
profil_bp = Blueprint("profil_bp", __name__)

# --------------------------------------------------------
# Route : /profil (GET et POST)
# Permet à l'utilisateur connecté de :
# - Voir ses informations (GET)
# - Mettre à jour son email ou son mot de passe (POST)
# --------------------------------------------------------
@profil_bp.route("/profil", methods=["GET", "POST"])
def profil():
    utilisateur = session.get("utilisateur")  # Vérifie si l'utilisateur est connecté
    if not utilisateur:
        return redirect("/login")  # Redirige vers login si non connecté

    message = None  # Message de retour à afficher (succès ou erreur)

    # Récupération de l'objet utilisateur depuis la base
    user = Utilisateur.query.filter_by(email=utilisateur['email']).first()

    # Si la méthode est POST, l'utilisateur veut modifier ses infos
    if request.method == 'POST':
        action = request.form.get("action")  # Type de modification ("email" ou "pwd")

        # === Modification de l'adresse email ===
        if action == "email":
            nouveau_email = request.form['nouveau_email'].strip().lower()

            # Validation du format email avec regex
            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                # Vérifie si l'email est déjà utilisé par un autre utilisateur
                if Utilisateur.query.filter_by(email=nouveau_email).first():
                    message = "❌ Cet email est déjà utilisé."
                else:
                    # Mise à jour en base et dans la session
                    user.email = nouveau_email
                    db.session.commit()
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."
            else:
                message = "❌ Email invalide."

        # === Modification du mot de passe ===
        elif action == "pwd":
            ancien  = request.form['ancien']   # Ancien mot de passe saisi
            nouveau = request.form['nouveau']  # Nouveau mot de passe
            confirm = request.form['confirm']  # Confirmation

            # Vérifie si l'ancien mot de passe est correct
            if user.mot_de_passe != ancien:
                message = "❌ Ancien mot de passe incorrect."
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                # Met à jour le mot de passe
                user.mot_de_passe = nouveau
                db.session.commit()
                message = "✅ Mot de passe modifié avec succès."

    # Affiche la page profil avec message si modification
    return render_template("profil.html", utilisateur=utilisateur, message=message)
