from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import re
from db import creer_base
from admin_creator import creer_admin
creer_base()
creer_admin()

app = Flask(__name__)
app.secret_key = 'cle-secrete-dylan'

def get_db():
    return sqlite3.connect("bibliotheque.db")

@app.route('/')
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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nom       = request.form['nom'].strip()
        email     = request.form['email'].strip().lower()
        pwd       = request.form['mot_de_passe']
        confirm   = request.form['confirmation']

        # Vérifier que les champs sont remplis
        if not nom or not email or not pwd:
            return render_template("signup.html", erreur="❌ Tous les champs sont obligatoires.")

        # Vérification basique email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template("signup.html", erreur="❌ Email invalide.")

        # Vérifier si l'email est déjà utilisé
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM utilisateurs WHERE email = ?", (email,))
        exist = cur.fetchone()

        if exist:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà inscrit.")

        # Correspondance des mots de passe
        if pwd != confirm:
            return render_template("signup.html", erreur="❌ Les mots de passe ne correspondent pas.")

        # Analyse du mot de passe
        niveau, niveau_label, remarques = evaluer_mot_de_passe(pwd)
        if niveau < 3:
            return render_template("signup.html", 
                                   erreur="❌ Mot de passe trop faible.",
                                   remarques=remarques,
                                   niveau=niveau_label)

        # Insérer en base
        try:
            cur.execute("""
                INSERT INTO utilisateurs (nom, email, mot_de_passe, is_admin)
                VALUES (?, ?, ?, 0)
            """, (nom, email, pwd))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("signup.html", erreur="❌ Cet email est déjà utilisé.")

        conn.close()

        # Connexion automatique après inscription
        session['utilisateur'] = {'nom': nom, 'email': email, 'is_admin': False}
        return redirect(url_for('livres'))

    # GET request
    return render_template("signup.html", niveau=None, remarques=[])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['mot_de_passe']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT nom, email, is_admin FROM utilisateurs WHERE email=? AND mot_de_passe=?", (email, mot_de_passe))
        user = cur.fetchone()
        conn.close()

        if user:
            session['utilisateur'] = {
                'nom': user[0],
                'email': user[1],
                'is_admin': bool(user[2])
            }
            return redirect('/')
        else:
            return render_template("login.html", erreur="❌ Identifiants incorrects")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect('/')

@app.route('/livres')
def livres():
    utilisateur = session.get('utilisateur')   # ← Récupère l’utilisateur connecté

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, titre, auteur, annee, exemplaires FROM livres")
    livres = cur.fetchall()
    conn.close()

    # ← Passe utilisateur au template
    return render_template("livres.html", livres=livres, utilisateur=utilisateur)

@app.route('/recherche')
def recherche():
    utilisateur = session.get('utilisateur')
    q = request.args.get('q', '').strip().lower()

    livres_resultat = []
    if q:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, titre, auteur, annee, exemplaires
            FROM livres
            WHERE LOWER(titre) LIKE ? OR LOWER(auteur) LIKE ?
        """, (f'%{q}%', f'%{q}%'))
        livres_resultat = cur.fetchall()
        conn.close()

    return render_template(
        "recherche.html",
        livres=livres_resultat,
        requete=q,
        utilisateur=utilisateur
    )


@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_livre():
    utilisateur = session.get("utilisateur")
    if not utilisateur or not utilisateur.get("is_admin"):
        return redirect('/')

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']
        exemplaires = request.form['exemplaires']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO livres (titre, auteur, annee, exemplaires)
            VALUES (?, ?, ?, ?)
        """, (titre, auteur, annee, exemplaires))
        conn.commit()
        conn.close()
        return redirect('/livres')

    return render_template("ajouter.html")

@app.route('/emprunter/<int:livre_id>', methods=['POST'])
def emprunter(livre_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    # Vérifier qu'il reste des exemplaires
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT exemplaires FROM livres WHERE id = ?", (livre_id,))
    result = cur.fetchone()
    if not result or result[0] <= 0:
        conn.close()
        # Option : afficher un message d’erreur (à implémenter plus tard)
        return redirect('/livres')

    # Enregistrer l'emprunt
    cur.execute("""
        INSERT INTO emprunts (utilisateur_email, livre_id)
        VALUES (?, ?)
    """, (utilisateur['email'], livre_id))
    # Décrémenter les exemplaires
    cur.execute("""
        UPDATE livres SET exemplaires = exemplaires - 1 WHERE id = ?
    """, (livre_id,))

    conn.commit()
    conn.close()

    return redirect('/livres')
@app.route('/mes_emprunts')
def mes_emprunts():
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, l.titre, l.auteur, e.date_emprunt
        FROM emprunts e
        JOIN livres l ON e.livre_id = l.id
        WHERE e.utilisateur_email = ?
    """, (utilisateur['email'],))
    emprunts = cur.fetchall()
    conn.close()

    return render_template("emprunter.html",
                           emprunts=emprunts)
                           

@app.route('/rendre/<int:emprunt_id>', methods=['POST'])
def rendre(emprunt_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    # Récupérer l’emprunt
    cur.execute("SELECT livre_id FROM emprunts WHERE id = ?", (emprunt_id,))
    row = cur.fetchone()
    if row:
        livre_id = row[0]
        # Supprimer l’emprunt
        cur.execute("DELETE FROM emprunts WHERE id = ?", (emprunt_id,))
        # Réaugmenter l’exemplaire
        cur.execute("UPDATE livres SET exemplaires = exemplaires + 1 WHERE id = ?", (livre_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('mes_emprunts'))

@app.route('/profil', methods=['GET', 'POST'])
def profil():
    utilisateur = session.get("utilisateur")
    if not utilisateur:
        return redirect('/login')

    message = None

    if request.method == 'POST':
        action = request.form.get("action")

        conn = get_db()
        cur = conn.cursor()

        if action == "email":
            nouveau_email = request.form['nouveau_email'].strip().lower()
            if re.match(r"[^@]+@[^@]+\.[^@]+", nouveau_email):
                try:
                    cur.execute("UPDATE utilisateurs SET email = ? WHERE email = ?", (nouveau_email, utilisateur['email']))
                    conn.commit()
                    session['utilisateur']['email'] = nouveau_email
                    message = "✅ Email mis à jour avec succès."
                except sqlite3.IntegrityError:
                    message = "❌ Cet email est déjà utilisé."
            else:
                message = "❌ Email invalide."

        elif action == "pwd":
            ancien = request.form['ancien']
            nouveau = request.form['nouveau']
            confirm = request.form['confirm']

            cur.execute("SELECT mot_de_passe FROM utilisateurs WHERE email = ?", (utilisateur['email'],))
            mdp_actuel = cur.fetchone()

            if not mdp_actuel or ancien != mdp_actuel[0]:
                message = "❌ Ancien mot de passe incorrect."
            elif nouveau != confirm:
                message = "❌ Les mots de passe ne correspondent pas."
            else:
                cur.execute("UPDATE utilisateurs SET mot_de_passe = ? WHERE email = ?", (nouveau, utilisateur['email']))
                conn.commit()
                message = "✅ Mot de passe modifié avec succès."

        conn.close()

    return render_template("profil.html", utilisateur=utilisateur, message=message)

if __name__ == "__main__":
    app.run(debug=True)
