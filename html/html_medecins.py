#!/bin/env python
# coding=utf-8
from dao import dao_personne
from dao import dao_medecin
from dao import dao_patient
from dao import dao_coordonnees
from dao import dao_question
from objects import medecin
from objects import personne
from objects import patient
from objects import question
from objects import coordonnees
from html import html_globale
import model_global

import cherrypy

class Pages_Medecins(html_globale.Page_Globale):


    def __init__(self):
        self.titre_page = "Espace médecins"

    def index(self):
        return super().connexion(self.titre_page)
    index.exposed = True


    def verif_connexion(self, login, passe) :
        med = dao_medecin.dao_Medecin().connexion(login, passe)
        if med == None :
            return super().connexion(self.titre_page) + "<div class='message_erreur'>Veuillez vérifier vous accès !</div>"
        else :
            pers = dao_personne.dao_Personne().get_personne(med.get_id_personne())
            #Stockage dans la session
            model_global.connect_user(model_global.user_type_medecin, med.get_id(), pers.get_nom(), pers.get_prenom(), pers.get_id())
            #Affichage de l'accueil patient connecté
            return self.accueil_medecin()
    verif_connexion.exposed = True

    #Liste des action
    def accueil_medecin(self):
        page = super().header()
        page = page + '''<ul>
            <li><a href="edit_medecin">Modifier mes infos personnelles</a></li>
            <li><a href="nouveau_medecin">Nouveau médecin</a></li>
            <li><a href="liste_medecins">Liste des médecins</a></li>
            <li><a href="ajouter_patient">Nouveau patient</a></li>
            <li><a href="liste_patients">Liste des patients</a></li>
            <li><a href="liste_questions">Liste des questions</a></li>
        </ul>'''
        page = page + super().footer()
        return page
    accueil_medecin.exposed = True

    #Formulaire pour ajouter un médecin
    def nouveau_medecin(self):
        page = super().header()
        page = page + '''
        <title>Créer un nouveau médecin</title>
        <h1>Créer un nouveau médecin</h1>
        <form action="enregistrer_medecin" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom"><br>

                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom"><br>

                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="daten"><br>

                <label for="e_mail">Adresse mail:</label>
                <input type="email" id="e_mail" name="mail"><br>

                <label for="rpps">Numéro RPPS:</label>
                <input type="number" id="rpps" name="rpps"><br>

                <label for="liberal">Libéral:</label>
                <input type="checkbox" id="liberal" name="liberal"><br>

                <label for="hopital">Hopital:</label>
                <input type="text" id="hopital" name="hopital"><br>

                <input type="submit" value="Enregistrer">
            </div>
        </form>
        '''
        page = page + super().footer()
        return page
    nouveau_medecin.exposed = True


    #Affiche la liste des medecins dans la base
    def liste_medecins(self):
        page = super().header()
        page = page + "Les des médecins : <a href='nouveau_medecin'>Ajouter</a>"
        liste = dao_medecin.dao_Medecin().get_all_medecins()
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit_medecin?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a>'
        page = page + super().footer()
        return page
    liste_medecins.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer_medecin(self, nom = "", prenom = "", daten = "", rpps = -1, liberal = False, hopital = "", mail=""):
        p = medecin.Medecin()
        p.set_nom(nom)
        p.set_prenom(prenom)
        p.set_date_de_naiss(daten)
        p.set_rpps(rpps)
        if liberal :
            p.set_liberal(True)
        else :
            p.set_liberal(False)
        p.set_hopital(hopital)
        coord = coordonnees.Coordonnees()
        coord.set_adresse_mail(mail)
        #Enregistrement et récupère l'id
        id = dao_medecin.dao_Medecin().insert_medecin(p)
        coord.set_id_personne(id)
        dao_coordonnees.dao_Coordonnees().insert_coordonnees(coord)
        #Recherche la personne dans la base
        pliste = dao_medecin.dao_Medecin().get_medecin(id)
        page = "Médecin ajouté : <br>"
        page = page + pliste.to_string()
        page = page + '''
        <form action="liste_medecins"><input type="submit" value="Liste des médecins"></form>
        '''
        return page
    enregistrer_medecin.exposed = True

    #Formulaire permettant de modifier les infos d'une personne
    def edit_medecin(self):
        id = model_global.get_user_id()
        page = super().header()
        page = page + "<h1>Edition d'un médecin</h1>"
        p = dao_medecin.dao_Medecin().get_medecin(id)
        page = page + '''
        <form action="update_medecin" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom" value="''' + p.get_nom() + '''"><br>
                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom" value="''' + p.get_prenom() + '''"><br>
                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="dateN" value="''' + str(p.get_date_de_naiss()) + '''"><br>
                <input type="submit" value="Modifier">
            </div>
        </form>
        '''
        return page
    edit_medecin.exposed = True

    #Met à jour les infos d'edition dans la base
    def update_medecin(self, nom, prenom, dateN):
        id = model_global.get_user_id()
        p = medecin.Medecin()
        p.set_id(id)
        p.set_nom(nom)
        p.set_prenom(prenom)
        p.set_date_de_naiss(dateN)
        #Enregistrement et récupère l'id
        dao_medecin.dao_Medecin().update_personne(p)
        #Recherche la personne dans la base
        pliste = dao_personne.dao_Personne().get_personne(id)
        page = pliste.to_string()
        return page
    update_medecin.exposed = True

    #Supprime la personne dans la base
    def supprimer(self, id):
        dao_personne.dao_Personne().delete_personne2(id)
        page = "Personne supprimée.<br>"
        page = page + self.liste_medecins()
        return page
    supprimer.exposed = True

    #Formulaire pour ajouter un patient
    def ajouter_patient(self):
        page = super().header()
        page = page + '''
        <title>Créer un nouveau patient</title>
        <h1>Créer un nouveau patient</h1>
        <form action="enregistrer_patient" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom_patient"><br>

                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom_patient"><br>

                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="date_patient"><br>

                <label for="nss">Numéro de Sécurité Sociale:</label>
                <input type="number" id="nss" name="nss"><br>

                <input type="submit" value="Enregistrer">
            </div>
        </form>
        '''
        page = page + super().footer()
        return page
    ajouter_patient.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer_patient(self, nom_patient, prenom_patient, date_patient, nss):
        p = patient.Patient()
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        p.set_nss(nss)
        p.set_id_medecin(model_global.get_user_id())
        #Enregistrement et récupère l'id
        id = dao_patient.dao_Patient().insert_patient(p)
        #Recherche la personne dans la base
        pliste = dao_patient.dao_Patient().get_patient(id)
        page = super().header()
        page = page + "<br>Nouveau patient : <br>"
        page = page + pliste.to_string()
        page = page + '''
        <form action="liste_patients"><input type="submit" value="Liste des patients"></form>
        '''
        page = page + super().footer()
        return page
    enregistrer_patient.exposed = True

    #Affiche la liste des medecins dans la base
    def liste_patients(self):
        page = super().header()
        page = page + "Les des patients : <a href='ajouter_patient'> Ajouter un patient</a>"
        liste = dao_patient.dao_Patient().get_all_patients()
        for c in liste :
            page = page + '<br>' + c.to_string() + ' <a href="edit?id=' + str(c.get_id())+'">Editer</a>'
        page = page + super().footer()
        return page
    liste_patients.exposed = True


    def liste_questions(self):
        page = super().header()
        page = page + "Liste des questions ici :"
        #Parametres du patients
        page = page + "<div>Paramêtres : <a href='nouveau_question?niveau=0'>Ajouter</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(0)
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit_question?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a><br>'
        page = page + "</ol></div>"
        #Questions symptomes frequents
        page = page + "<div>Fréquent : <a href='nouveau_question?niveau=1'>Ajouter</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(1)
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit_question?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a><br>'
        page = page + "</ol></div>"

        #Questions symptomes moins frequents
        page = page + "<div>Moins Fréquent : <a href='nouveau_question?niveau=2'>Ajouter</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(2)
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit_question?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a><br>'
        page = page + "</ol></div>"

        #Questions symptomes frequents
        page = page + "<div>Grave : <a href='nouveau_question?niveau=3'>Ajouter</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(3)
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit_question?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a><br>'
        page = page + "</ol></div>"
        page = page + '<a href="accueil_medecin">Accueil</a>'
        page = page + super().footer()
        return page
    liste_questions.exposed = True


    def nouveau_question(self, niveau):
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Ajouter une question
        </legend>'''
        page = page + '''
        <form action="enregistrer_question" method="GET">
            <div>
                <label for="intitule">Intitulé:</label><br>
                <textarea id="intitule" name="intitule" rows="2" cols="50"></textarea><br>

                <label for="description">Déscription:</label><br>
                <textarea id="description" name="description" rows="4" cols="50"></textarea><br>

                <label for="valeur">Réponse par défaut:</label><br>
                <textarea id="valeur" name="valeur" rows="2" cols="50"></textarea><br>

                <label for="reponse_alerte">Réponse alerte:</label><br>
                <input type="text" id="reponse_alerte" name="reponse_alerte">
                <select name="comparateur" id="comparateur">
                    <option value=0 >Plus grand</option>
                    <option value=1 >Plus petit</option>
                    <option value=2 selected>Egale</option>
                </select>
                <br>
                <label for="type_reponse">Type de réponse :</label>
                <select name="type_reponse" id="type_reponse">
                    <option value="Texte" selected >Texte</option>
                    <option value="Numérique" selected >Numérique</option>
                </select>

                <label for="niveau">Niveau :</label>
                <select name="niveau" id="niveau">'''
        if niveau == '0' :
            page = page + "<option value=0 selected >Paramêtres</option>"
        else :
            page = page + "<option value=0>Paramêtres</option>"

        if niveau == '1' :
            page = page + "<option value=1 selected >Fréquent</option>"
        else :
            page = page + "<option value=1>Fréquent</option>"

        if niveau == '2' :
            page = page + "<option value=2 selected > Moins fréquent</option>"
        else :
            page = page + "<option value=2>Moins fréquent</option>"

        if niveau == '3' :
            page = page + "<option value=3 selected >Grave</option>"
        else :
            page = page + "<option value=3>Grave</option>"

        page = page + '''</select>
                <input type="submit" value="Enregistrer">
            </div>
        </form>
        </fieldset>'''
        page = page + super().footer()
        return page
    nouveau_question.exposed = True


    def enregistrer_question(self, niveau, intitule, description, valeur, type_reponse, reponse_alerte, comparateur):
        dao_question.dao_Question().insert_question2(intitule, description, valeur, niveau, type_reponse, reponse_alerte, comparateur)
        return self.liste_questions()
    enregistrer_question.exposed = True