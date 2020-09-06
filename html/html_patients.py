#!/bin/env python
# coding=utf-8
import cherrypy
from time import gmtime, strftime
from time import time

from dao import dao_patient
from dao import dao_personne
from dao import dao_question
from dao import dao_reponse
from dao import dao_questionnaire
from objects import patient
from objects import personne
from objects import question
from objects import reponse
from objects import questionnaire
from html import html_globale
import model_global

class Pages_Patients(html_globale.Page_Globale) :

    def __init__(self):
        self.titre_page = "Espace patients"
        self.rubrique = 0
        #Liste des questions
        self.liste_parametres = []
        self.liste_sympt_frequents = []
        self.liste_sympt_moins_frequents = []
        self.liste_sympt_graves = []
        #Liste des réponses
        self.reponses_parametres = []
        self.reponses_sympt_frequents = []
        self.reponses_sympt_moins_frequents = []
        self.reponses_sympt_graves = []
        self.date = ""
        self.date_time_quest = None
        self.questionnaire_jour = questionnaire.Questionnaire()


    def index(self):
        return self.connexion(self.titre_page)
    index.exposed = True

    def verif_connexion(self, login, passe) :
        patient = dao_patient.dao_Patient().connexion(login, passe)
        if patient == None :
            return super().connexion(self.titre_page) + "<div class='message_erreur'>Veuillez vérifier vous accès !</div>"
        else :
            pers = dao_personne.dao_Personne().get_personne(patient.get_id_personne())
            #Stockage dans la session
            model_global.connect_user(model_global.user_type_patient, patient.get_id(), pers.get_nom(), pers.get_prenom(), pers.get_id())
            #Affichage de l'accueil patient connecté
            self.date_time_quest = gmtime()
            page = self.accueil_patient()
        return page
    verif_connexion.exposed = True


    def accueil_patient(self):
        page = super().header()
        page = page + '''<fieldset class="cadre">
            <legend>
                Espace personnel
            </legend>'''
        page = page + '''<ul>
        <li><a href="evolution_patient">Voir mon évolution</a></li>
        <li><a href="questionnaire_patient">Questionnaire</a></li>
        <li><a href="edition_patient">Modifier mes informations personnelles</a></li>
        </ul></fieldset>'''
        page = page + super().footer()
        return page
    accueil_patient.exposed = True


    #Construit les listes de réponses pour stoquer les saisies du patient avant d'enregistrer dans la base
    def init_listes_questions(self):
        #Les paramêtres
        self.liste_parametres = dao_question.dao_Question().get_questions_niveau(0)
        id_patient = model_global.get_user_id()

        self.reponses_parametres = dao_reponse.dao_Reponse().get_last_reponse_patient(id_patient, 0)
        if len(self.reponses_parametres) == 0 :
            self.liste_parametres = dao_question.dao_Question().get_questions_niveau(0)
            self.reponses_parametres = []
            for quest in self.liste_parametres :
                rep = reponse.Reponse()
                rep.set_id_question(quest.get_id())
                rep.set_reponse(quest.get_valeur())
                self.reponses_parametres.append(rep)

        #Symptomes fréquents
        self.liste_sympt_frequents = dao_question.dao_Question().get_questions_niveau(1)
        self.reponses_sympt_frequents = dao_reponse.dao_Reponse().get_last_reponse_patient(id_patient, 1)
        if len(self.reponses_sympt_frequents) == 0 :
            self.liste_sympt_frequents = dao_question.dao_Question().get_questions_niveau(1)
            self.reponses_sympt_frequents = []
            for quest in self.liste_sympt_frequents :
                rep = reponse.Reponse()
                rep.set_id_question(quest.get_id())
                rep.set_reponse(quest.get_valeur())
                self.reponses_sympt_frequents.append(rep)

        #Symptomes moins fréquents
        self.liste_sympt_moins_frequents = dao_question.dao_Question().get_questions_niveau(2)
        self.reponses_sympt_moins_frequents = dao_reponse.dao_Reponse().get_last_reponse_patient(id_patient, 2)
        if len(self.reponses_sympt_moins_frequents) == 0 :
            self.liste_sympt_moins_frequents = dao_question.dao_Question().get_questions_niveau(2)
            self.reponses_sympt_moins_frequents = []
            for quest in self.liste_sympt_moins_frequents :
                rep = reponse.Reponse()
                rep.set_id_question(quest.get_id())
                rep.set_reponse(quest.get_valeur())
                self.reponses_sympt_moins_frequents.append(rep)

        #Symptomes graves
        self.liste_sympt_graves = dao_question.dao_Question().get_questions_niveau(3)
        self.reponses_sympt_graves = dao_reponse.dao_Reponse().get_last_reponse_patient(id_patient, 3)
        if len(self.reponses_sympt_graves) == 0 :
            self.liste_sympt_graves = dao_question.dao_Question().get_questions_niveau(3)
            self.reponses_sympt_graves = []
            for quest in self.liste_sympt_graves :
                rep = reponse.Reponse()
                rep.set_id_question(quest.get_id())
                rep.set_reponse(quest.get_valeur())
                self.reponses_sympt_graves.append(rep)

        #Commentaire
        quest = dao_questionnaire.dao_Questionnaire().get_last_questionnaire(id_patient)
        if not (quest == None) :
            self.questionnaire_jour.set_commentaire(quest.get_commentaire())

    init_listes_questions.exposed = True

    #Affcihe le questionnaire du jour
    def questionnaire_patient(self):
        self.init_listes_questions()
        self.date = strftime("%d / %m / %Y à %Hh%M", self.date_time_quest)
        self.rubrique = 0
        dateQ = strftime("%Y-%m-%d", self.date_time_quest)
        heureQ = strftime("%H:%M", self.date_time_quest)
        self.questionnaire_jour.set_date(dateQ)
        self.questionnaire_jour.set_heure(heureQ)

        page = self.affiche_rubrique_courant()
        return page
    questionnaire_patient.exposed = True

    #Rubrique saisie des parametres
    def questions_parametres(self, rubrique = 0, edit = -1):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaire du jour : ''' + self.date + '''
        </legend>'''
        page = page + '''<div>
                    <div class="rubriques">
                        <div class="button_selected"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                        <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                        <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                        <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
                    </div>
                    <div class="liste_questions">'''

        page = page + "<div>"
        count = 0
        for i in range(len(self.liste_parametres)) :
            c = self.liste_parametres[i]
            rep = self.reponses_parametres[i]
            #Mode edition
            if int(count) == int(edit) :
                page = page + "<form action='enregistrer_question' method='GET'>"
                page = page + '<br><label for="reponse"><b>' + c.get_intitule() + '</b></label>'
                page = page + "<br>Déscription:"+c.get_description()
                page = page + '<br>Réponse : '
                page = page + '<input type="hidden" name="id" value="' + str(c.get_id()) + '">'
                if c.get_type_reponse() == "Numérique" :
                    page = page + '<input type="number" id="reponse" name="reponse" value="' + str(rep.get_reponse()) + '">'
                else :
                    page = page + '<br><textarea id="reponse" name="reponse" rows="2" cols="40" >' + rep.get_reponse() + '</textarea>'
                page = page + '<input type="submit" value="V">'
                page = page + "</form>"
            else :
                #mode affichage
                page = page + c.get_intitule() + " : " + rep.get_reponse() + ' <a href="questions_parametres?edit=' + str(count) + '">'
                page = page +'<img src="/annexes/image_edit.png" alt="Edit"/></a><br>'
            count = count + 1

        page = page + "</div>"
        page = page + " </div>"
        page = page + '<div class="bouton_bas"><div class="button_suiv"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div></div></div></fieldset>'
        page = page + super().footer()
        return page
    questions_parametres.exposed = True

    #Rubrique saisie des parametres
    def questions_sympt_frequents(self, rubrique = 1, edit = -1):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaire du jour : ''' + self.date + '''
        </legend>'''
        page = page + '''<div>
            <div class="rubriques">
                <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                <div class="button_selected"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
            </div>
            <div class="liste_questions">'''

        page = page + "<div>"
        count = 0
        for i in range(len(self.liste_sympt_frequents)) :
            c = self.liste_sympt_frequents[i]
            rep = self.reponses_sympt_frequents[i]
            #Mode edition
            if int(count) == int(edit) :
                page = page + "<form action='enregistrer_question' method='GET'>"
                page = page + '<br><label for="reponse"><b>' + c.get_intitule() + '</b></label>'
                page = page + "<br>Déscription:"+c.get_description()
                page = page + '<br>Réponse : '
                page = page + '<input type="hidden" name="id" value="' + str(c.get_id()) + '">'
                if c.get_type_reponse() == "Numérique" :
                    page = page + '<input type="number" id="reponse" name="reponse" value="' + str(rep.get_reponse()) + '">'
                else :
                    page = page + '<br><textarea id="reponse" name="reponse" rows="2" cols="40" >' + rep.get_reponse() + '</textarea>'
                page = page + '<input type="submit" value="V">'
                page = page + "</form>"
            else :
                #mode affichage
                page = page + c.get_intitule() + " : " + rep.get_reponse() + ' <a href="questions_sympt_frequents?edit=' + str(count) + '">'
                page = page +'<img src="/annexes/image_edit.png" alt="Edit"/></a><br>'
            count = count + 1

        page = page + "</div>"
        page = page + " </div>"
        page = page + '''<div class="bouton_bas"><div class="button_preced"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
        <div class="button_suiv"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div></div></div></fieldset>'''
        page = page + super().footer()
        return page
    questions_sympt_frequents.exposed = True

    #Sympt moins frequents
    def questions_sympt_moins_frequents(self, rubrique = 2, edit = -1):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaire du jour : ''' + self.date + '''
        </legend>'''
        page = page + '''<div>
            <div class="rubriques">
                <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                <div class="button_selected"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
            </div>
            <div class="liste_questions">'''

        page = page + "<div>"
        count = 0
        for i in range(len(self.liste_sympt_moins_frequents)) :
            c = self.liste_sympt_moins_frequents[i]
            rep = self.reponses_sympt_moins_frequents[i]
            #Mode edition
            if int(count) == int(edit) :
                page = page + "<form action='enregistrer_question' method='GET'>"
                page = page + '<br><label for="reponse"><b>' + c.get_intitule() + '</b></label>'
                page = page + "<br>Déscription:"+c.get_description()
                page = page + '<br>Réponse : '
                page = page + '<input type="hidden" name="id" value="' + str(c.get_id()) + '">'
                if c.get_type_reponse() == "Numérique" :
                    page = page + '<input type="number" id="reponse" name="reponse" value="' + str(rep.get_reponse()) + '">'
                else :
                    page = page + '<br><textarea id="reponse" name="reponse" rows="2" cols="40" >' + rep.get_reponse() + '</textarea>'
                page = page + '<input type="submit" value="V">'
                page = page + "</form>"
            else :
                #mode affichage
                page = page + c.get_intitule() + " : " + rep.get_reponse() + ' <a href="questions_sympt_moins_frequents?edit=' + str(count) + '">'
                page = page +'<img src="/annexes/image_edit.png" alt="Edit"/></a><br>'
            count = count + 1

        page = page + "</div>"
        page = page + " </div>"
        page = page + '''<div class="bouton_bas"><div class="button_preced"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
        <div class="button_suiv"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div></div></div></fieldset>'''
        page = page + super().footer()
        return page
    questions_sympt_moins_frequents.exposed = True

    #Sympt graves
    def questions_sympt_graves(self, rubrique = 3, edit = -1):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaire du jour : ''' + self.date + '''
        </legend>'''
        page = page + '''<div>
            <div class="rubriques">
                <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                <div class="button_selected"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
            </div>
            <div class="liste_questions">'''

        page = page + "<div>"
        count = 0
        for i in range(len(self.liste_sympt_graves)) :
            c = self.liste_sympt_graves[i]
            rep = self.reponses_sympt_graves[i]
            #Mode edition
            if int(count) == int(edit) :
                page = page + "<form action='enregistrer_question' method='GET'>"
                page = page + '<br><label for="reponse"><b>' + c.get_intitule() + '</b></label>'
                page = page + "<br>Déscription:"+c.get_description()
                page = page + '<br>Réponse : '
                page = page + '<input type="hidden" name="id" value="' + str(c.get_id()) + '">'
                if c.get_type_reponse() == "Numérique" :
                    page = page + '<input type="number" id="reponse" name="reponse" value="' + str(rep.get_reponse()) + '">'
                else :
                    page = page + '<br><textarea id="reponse" name="reponse" rows="2" cols="40" >' + rep.get_reponse() + '</textarea>'
                page = page + '<input type="submit" value="V">'
                page = page + "</form>"
            else :
                #mode affichage
                page = page + c.get_intitule() + " : " + rep.get_reponse() + ' <a href="questions_sympt_graves?edit=' + str(count) + '">'
                page = page +'<img src="/annexes/image_edit.png" alt="Edit"/></a><br>'
            count = count + 1

        #Commentaire du questionnaire
        if int(edit) == 1000 :
            page = page + "<form action='enregistrer_commentaire' method='GET'>"
            page = page + '<br><label for="reponse"><b>Commentaire</b></label>'
            page = page + '<br>Réponse : '
            page = page + '<br><textarea id="reponse" name="reponse" rows="2" cols="40" >'+ self.questionnaire_jour.get_commentaire() + '</textarea>'
            page = page + '<input type="submit" value="V">'
            page = page + "</form>"
        else :
            #mode affichage
            page = page + "Commentaire : " + self.questionnaire_jour.get_commentaire() + ' <a href="questions_sympt_graves?edit=1000">'
            page = page +'<img src="/annexes/image_edit.png" alt="Edit"/></a><br>'



        page = page + "</div>"
        page = page + " </div>"
        page = page + '<div class="bouton_bas"><div class="button_preced"><div><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>'
        page = page + '<div class="button_suiv"><a href="valider_questionnaire">VALIDER</a></div></div>'
        page = page + '</div></div></fieldset>'
        page = page + super().footer()
        return page
    questions_sympt_graves.exposed = True

    #Affichage de la rubrique
    def affiche_rubrique_courant(self):
        page = ""
        if self.rubrique == 0 :
            page = page + self.questions_parametres()

        elif self.rubrique == 1 :
            page = page + self.questions_sympt_frequents()

        elif self.rubrique == 2 :
            page = page + self.questions_sympt_moins_frequents()

        elif self.rubrique == 3 :
            page = page + self.questions_sympt_graves()

        return page
    affiche_rubrique_courant.exposed = True


    #Enregistre le commentaire du questionnaire
    def enregistrer_commentaire(self, reponse) :
        self.questionnaire_jour.set_commentaire(reponse)
        page = self.affiche_rubrique_courant()
        return page
    enregistrer_commentaire.exposed = True

    #Enregistrement de la saisie
    def enregistrer_question(self, id, reponse):
        page = "Page introuvable !!!"
        if self.rubrique == 0:
            rep = None
            for rep in self.reponses_parametres :
                if rep.get_id_question() == int(id):
                    rep.set_reponse(reponse)
            page = self.affiche_rubrique_courant()

        elif self.rubrique == 1:
            rep = None
            for rep in self.reponses_sympt_frequents :
                if rep.get_id_question() == int(id):
                    rep.set_reponse(reponse)
            page = self.affiche_rubrique_courant()

        elif self.rubrique == 2:
            rep = None
            for rep in self.reponses_sympt_moins_frequents :
                if rep.get_id_question() == int(id):
                    rep.set_reponse(reponse)
            page = self.affiche_rubrique_courant()

        elif self.rubrique == 3:
            rep = None
            for rep in self.reponses_sympt_graves :
                if rep.get_id_question() == int(id):
                    rep.set_reponse(reponse)
            page = self.affiche_rubrique_courant()

        return page
    enregistrer_question.exposed = True


    def valider_questionnaire(self):
        id_patient = model_global.get_user_id()
        self.questionnaire_jour.set_id_patient(id_patient)
        #enregistrer questionnaire
        idques = dao_questionnaire.dao_Questionnaire().insert_questionnaire(self.questionnaire_jour)
        #Enregistrer les responses
        for rep in self.reponses_parametres :
            rep.set_id_questionnaire(idques)
            dao_reponse.dao_Reponse().insert_reponse(rep)

        for rep in self.reponses_sympt_frequents :
            rep.set_id_questionnaire(idques)
            dao_reponse.dao_Reponse().insert_reponse(rep)

        for rep in self.reponses_sympt_moins_frequents :
            rep.set_id_questionnaire(idques)
            dao_reponse.dao_Reponse().insert_reponse(rep)

        for rep in self.reponses_sympt_graves :
            rep.set_id_questionnaire(idques)
            dao_reponse.dao_Reponse().insert_reponse(rep)

        #page =  str(idques) + "; " + str(self.questionnaire_jour.get_date()) + "; " + str(self.questionnaire_jour.get_heure()) + "; " + str(self.questionnaire_jour.get_id_patient())
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaire du jour : ''' + self.date + '''
        </legend>'''
        page = page + 'Votre questionnaire a bien été validé !<br><a href="accueil_patient">Retour accueil</a>'
        page = page + "</fieldset>"
        page = page + super().footer()
        return page
    valider_questionnaire.exposed = True

    #Formulaire permettant de modifier les infos d'une personne
    def edition_patient(self):
        page = "<h1>Edition d'une personne</h1>"
        p = dao_patient.dao_Patient().get_patient(model_global.get_user_id())
        page = page + '''
        <form action="update" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom_patient" value="'''+p.get_nom()+ '''"><br>
                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom_patient" value="'''+p.get_prenom()+ '''"><br>
                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="date_patient" value="'''+p.get_date_de_naiss()+ '''"><br>
                <label for="nss">Numéro de Sécurité Sociale:</label>
                <input type="number" id="nss" name="nss" value="'''+str(p.get_nss())+ '''"><br>
                <input type="submit" value="Modifier">
            </div>
        </form>
        '''
        return page
    edition_patient.exposed = True

    #Met à jour les infos d'edition dans la base
    def update(self, nom_patient, prenom_patient, date_patient):
        p = personne.Personne()
        p.set_id(model_global.get_user_id())
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        #Enregistrement et récupère l'id
        dao_personne.dao_Personne().update_personne(p)
        #Recherche la personne dans la base
        pliste = dao_personne.dao_Personne().get_personne(model_global.get_user_id())
        page = pliste.to_string()
        return page
    update.exposed = True

    #Supprime la personne dans la base
    def supprimer(self, id):
        dao_personne.dao_Personne().delete_personne2(id)
        page = "Personne supprimée.<br>"
        return page
    supprimer.exposed = True
