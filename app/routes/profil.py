from flask import Blueprint, render_template, request, session, redirect, url_for
import mysql.connector
import re

# Création du blueprint pour la gestion du profil utilisateur
profil_bp = Blueprint("profil_bp", __name__)

# Fonction pour établir la connexion à la base MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

# Route pour afficher ou modifier le profil
@profil_bp.route("/profil", methods=["GET", "POST"])
def profil():
    utilisateur = session.get("utilisateur")  # Vérifie que l'utilisateur est connecté
    if not utilisateur:
        return redirect("/login")  # Redirige vers la page de connexion si non connecté

    message = None  # Message de confirmation ou d'erreur à afficher

    if request.method == 'POST':
        action = request.form.get("action")  # Peut être "email" ou "pwd"

        conn = get_db()
        cur = conn.cursor()

        # --- Modification de l'adresse email ---
        if action == "email":
            nouveau_email = request.form['nouveau_email'].strip().lower()

            # Vérifie le format de l'email
            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                try:
                    # Mise à jour de l'email dans la base
                    cur.execute("UPDATE utilisateurs SET email = %s WHERE email = %s",
                                (nouveau_email, utilisateur['email']))
                    conn.commit()

                    # Met à jour l'email dans la session
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."
                except mysql.connector.IntegrityError:
                    message = "❌ Cet email est déjà utilisé."
            else:
                message = "❌ Email invalide."

        # --- Modification du mot de passe ---
        elif action == "pwd":
            ancien  = request.form['ancien']
            nouveau = request.form['nouveau']
            confirm = request.form['confirm']

            # Vérifie l'ancien mot de passe
            cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = %s", (utilisateur['email'],))
            mdp_actuel = cur.fetchone()

            if not mdp_actuel or ancien != mdp_actuel[0]:
                message = "❌ Ancien mot de passe incorrect."
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                # Met à jour le mot de passe dans la base
                cur.execute("UPDATE utilisateurs SET mot_de_passe = %s WHERE email = %s",
                            (nouveau, utilisateur['email']))
                conn.commit()
                message = "✅ Mot de passe modifié avec succès."

        conn.close()

    # Affiche la page profil avec les infos et le message
    return render_template("profil.html", utilisateur=utilisateur, message=message)
