from flask import Blueprint, render_template, request, redirect, session, url_for
from datetime import datetime, timedelta
from app.models.db import db, Livre, Emprunt
from app.models.mail import envoyer_email

livres_bp = Blueprint('livres', __name__)

@livres_bp.route('/livres')
def livres():
    utilisateur = session.get('utilisateur')
    tous_les_livres = Livre.query.all()
    return render_template("livres.html", livres=tous_les_livres, utilisateur=utilisateur)

@livres_bp.route('/recherche')
def recherche():
    utilisateur = session.get('utilisateur')
    q = request.args.get('q', '').strip().lower()

    livres_resultat = []
    if q:
        livres_resultat = Livre.query.filter(
            (Livre.titre.ilike(f'%{q}%')) | (Livre.auteur.ilike(f'%{q}%'))
        ).all()

    return render_template("recherche.html", livres=livres_resultat, requete=q, utilisateur=utilisateur)

@livres_bp.route('/ajouter', methods=['GET', 'POST'])
def ajouter_livre():
    utilisateur = session.get("utilisateur")
    if not utilisateur or not utilisateur.get("is_admin"):
        return redirect('/')

    if request.method == 'POST':
        livre = Livre(
            titre=request.form['titre'],
            auteur=request.form['auteur'],
            annee=request.form['annee'],
            exemplaires=int(request.form['exemplaires'])
        )
        db.session.add(livre)
        db.session.commit()
        return redirect('/livres')

    return render_template("ajouter.html")

@livres_bp.route('/emprunter/<int:livre_id>', methods=['POST'])
def emprunter(livre_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    livre = db.session.get(Livre, livre_id)

    if not livre or livre.exemplaires <= 0:
        return redirect('/livres')

    # Création de l’emprunt
    date_limite = datetime.utcnow().date() + timedelta(days=7)
    emprunt = Emprunt(
        utilisateur_email=utilisateur['email'],
        livre_id=livre.id,
        date_limite=date_limite
    )
    db.session.add(emprunt)

    # Mise à jour du stock
    livre.exemplaires -= 1
    db.session.commit()

    # Envoi de l’email
    sujet = "📚 Confirmation d’emprunt de livre"
    contenu = f"""Bonjour {utilisateur['nom']},

Vous avez emprunté le livre : {livre.titre}
📅 Date d'emprunt : {datetime.utcnow().date()}
📆 Date limite de retour : {date_limite}

Merci de respecter cette date pour éviter une pénalité.

Cordialement,
La Bibliothèque
"""
    envoyer_email(utilisateur['email'], sujet, contenu)

    return redirect('/livres')

@livres_bp.route('/mes_emprunts')
def mes_emprunts():
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    emprunts = db.session.query(
        Emprunt.id,
        Livre.titre,
        Livre.auteur,
        Emprunt.date_emprunt,
        Emprunt.date_limite
    ).join(Livre, Emprunt.livre_id == Livre.id)\
     .filter(Emprunt.utilisateur_email == utilisateur['email'])\
     .all()

    return render_template("emprunter.html", emprunts=emprunts)

@livres_bp.route('/rendre/<int:emprunt_id>', methods=['POST'])
def rendre(emprunt_id):
    utilisateur = session.get('utilisateur')
    if not utilisateur:
        return redirect('/login')

    emprunt = Emprunt.query.get(emprunt_id)
    if emprunt:
        livre = Livre.query.get(emprunt.livre_id)
        if livre:
            livre.exemplaires += 1
        db.session.delete(emprunt)
        db.session.commit()

    return redirect(url_for('livres.mes_emprunts'))
