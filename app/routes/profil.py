from flask import Blueprint, render_template, request, session, redirect, url_for
import mysql.connector
import re

profil_bp = Blueprint("profil_bp", __name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="dylan",
        password="dylan@2005",
        database="bibliotheque"
    )

@profil_bp.route("/profil", methods=["GET", "POST"])
def profil():
    utilisateur = session.get("utilisateur")
    if not utilisateur:
        return redirect("/login")

    message = None

    if request.method == 'POST':
        action = request.form.get("action")

        conn = get_db()
        cur = conn.cursor()

        if action == "email":
            nouveau_email = request.form['nouveau_email'].strip().lower()
            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                try:
                    cur.execute("UPDATE utilisateurs SET email = %s WHERE email = %s", (nouveau_email, utilisateur['email']))
                    conn.commit()
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."
                except mysql.connector.IntegrityError:
                    message = "❌ Cet email est déjà utilisé."
            else:
                message = "❌ Email invalide."

        elif action == "pwd":
            ancien = request.form['ancien']
            nouveau = request.form['nouveau']
            confirm = request.form['confirm']

            cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = %s", (utilisateur['email'],))
            mdp_actuel = cur.fetchone()

            if not mdp_actuel or ancien != mdp_actuel[0]:
                message = "❌ Ancien mot de passe incorrect."
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                cur.execute("UPDATE utilisateurs SET mot_de_passe = %s WHERE email = %s", (nouveau, utilisateur['email']))
                conn.commit()
                message = "✅ Mot de passe modifié avec succès."

        conn.close()

    return render_template("profil.html", utilisateur=utilisateur, message=message)
