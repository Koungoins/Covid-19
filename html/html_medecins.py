#!/bin/env python
# coding=utf-8
from time import gmtime, strftime, localtime
from time import time
from dao import dao_personne
from dao import dao_medecin
from dao import dao_patient
from dao import dao_coordonnees
from dao import dao_question
from dao import dao_reponse
from dao import dao_questionnaire
from objects import medecin
from objects import personne
from objects import patient
from objects import reponse
from objects import question
from objects import questionnaire
from objects import coordonnees
from html import html_page
import model_global

import cherrypy

class Pages_Medecins(html_page.Page_html):


    def __init__(self):
        self.titre_page = "Espace médecins"
        self.rubrique = 0
        self.patient_selected = -1

    def index(self):
        return super().connexion(self.titre_page, 1)
    index.exposed = True

    def verif_connexion(self, login, passe) :
        med = dao_medecin.dao_Medecin().connexion(login, passe)
        if med == None :
            return super().connexion(self.titre_page, 1) + "<div class='message_erreur'>Veuillez vérifier vous accès !</div>"
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
        page = page + '''<fieldset class="cadre">
        <legend>
            Accueil
        </legend>
        <div>'''
        page = page + "<ul>"
        liste = dao_patient.dao_Patient().get_patients_medecin_non_analyses(model_global.get_user_id())
        if len(liste)>0 :
            page = page + '''<li class="button_vert"><a href="questionnaires_non_analyses">Questionnaires non analysés</a></li>'''
        page = page + '''<li class="button_vert"><a href="ajouter_patient">Nouveau patient</a></li>
            <li class="button_vert"><a href="liste_patients">Liste des patients</a></li>
            <li class="button_vert"><a href="liste_questions">Liste des questions</a></li>
            <li class="button_vert"><a href="liste_medecins">Liste des médecins</a></li>
            <li class="button_vert"><a href="edit_medecin">Modifier mes informations personnelles</a></li>
        </ul></div></fieldset>'''
        page = page + super().footer()
        return page
    accueil_medecin.exposed = True

    #Formulaire pour ajouter un médecin
    def nouveau_medecin(self):
        page = super().entete()
        page = page + '''<fieldset class="cadre">
        <legend>
            Inscription nouveau médecin
        </legend>
        <div class="box">'''
        page = page + '''
        <form action="enregistrer_medecin" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom"><br>

                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom"><br>

                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="daten"><br>

                <label for="rpps">Numéro RPPS:</label>
                <input type="number" id="rpps" name="rpps"><br>

                <label for="liberal">Libéral:</label>
                <input type="checkbox" id="liberal" name="liberal"><br>

                <label for="hopital">Hopital:</label>
                <input type="text" id="hopital" name="hopital"><br>

                <label for="adresse_postale">Adresse postale:</label><br>
                <textarea id="adresse_postale" name="adresse_postale" rows="3" cols="50" ></textarea><br>

                <label for="tel">Numéro de téléphone:</label>
                <input type="tel" id="phone" name="telephone" pattern="[0-9]{10}"><br>

                <label for="e_mail">Adresse mail:</label>
                <input type="email" id="e_mail" name="e_mail"><br>

                <input type="submit" value="Enregistrer" class="button_vert">
            </div>
        </form>
        </div></fieldset>
        '''
        page = page + super().footer()
        return page
    nouveau_medecin.exposed = True


    #Affiche la liste des medecins dans la base
    def liste_medecins(self):
        page = super().entete()
        page = page + '''<fieldset class="cadre">
        <legend>
            Les des médecins enregistrés
        </legend>
        <div class="box">'''
        liste = dao_medecin.dao_Medecin().get_all_medecins()
        count = 1
        page = page + "<table>"
        page = page + "<tr><th>Nom prénom</th><th>Cabinet</th><th>Téléphone</th></tr>"
        for c in liste :
            if count % 2 == 0:
                page = page + '<tr>'
            else :
                page = page + "<tr class='ligne_gris'>"
            coord = dao_coordonnees.dao_Coordonnees().get_coordonnees_personne(c.get_id_personne())
            tel = ""
            if not (coord == None) :
                tel = coord.get_telephone()
            page = page + '<td>' + c.get_nom() + " " + c.get_prenom() + '</td><td>' + c.get_hopital() +'</td><td>' + tel + '</td></tr>'
            count = count + 1 
        page = page + "</table>"
        page = page + '''</div></fieldset><a href="accueil_medecin">Retour accueil</a>'''
        page = page + super().footer()
        return page
    liste_medecins.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer_medecin(self, nom="", prenom="", daten="", rpps="", liberal="off", hopital="", adresse_postale="", telephone="", e_mail=""):
        print("Liberal:" + liberal)
        p = medecin.Medecin()
        p.set_nom(nom)
        p.set_prenom(prenom)
        p.set_date_de_naiss(daten)
        p.set_rpps(rpps)
        if liberal == "on" :
            p.set_liberal(True)
        else :
            p.set_liberal(False)
        p.set_hopital(hopital)
        coord = coordonnees.Coordonnees()
        coord.set_adresse_mail(e_mail)
        coord.set_adresse_postale(adresse_postale)
        coord.set_telephone(telephone)
        #Enregistrement et récupère l'id
        id = dao_medecin.dao_Medecin().insert_medecin(p)
        coord.set_id_personne(id)
        dao_coordonnees.dao_Coordonnees().insert_coordonnees(coord)
        #Recherche la personne dans la base
        pliste = dao_medecin.dao_Medecin().get_medecin(id)
        page = super().entete()
        page = page + '''<fieldset class="cadre">
        <legend>
            Créer un nouveau médecin
        </legend>
        <div class="box">'''
        page = page + "Bonjour docteur <b>" + pliste.get_nom() + " " + pliste.get_prenom() + "</b><br>"
        page = page + "Vous faite maintenant intégré à la plateforme de suivi quotidient de patients Covid-19.<br>"
        page = page + "Ci dessous, vos accès pour vous identifier :<br>"
        page = page + super().get_acces_utilisateur(pliste.get_id_personne())
        page = page + "<br>Veuillez à ne pas les égarer."
        page = page + '''
        <a href="/medecins/">Connexion</a>
        </div></fieldset>'''
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
                <input type="submit" value="Modifier" class="button_vert">
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
        page = page + '''<fieldset class="cadre">
        <legend>
            Créer un nouveau patient
        </legend>
        <div>'''
        page = page + '''
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

                <label for="adresse_postale">Adresse postale:</label><br>
                <textarea id="adresse_postale" name="adresse_postale" rows="3" cols="50" ></textarea><br>

                <label for="tel">Numéro de téléphone:</label>
                <input type="tel" id="phone" name="telephone" pattern="[0-9]{10}"><br>

                <label for="e_mail">Adresse mail:</label>
                <input type="email" id="e_mail" name="e_mail"><br>

                 <label for="date_teste">Date du teste:</label>
                <input type="date" id="date_teste" name="date_teste"><br>

                <input type="submit" value="Enregistrer" class="button_vert">
            </div>
        </form>
        </div></fieldset>'''
        page = page + super().footer()
        return page
    ajouter_patient.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer_patient(self, nom_patient, prenom_patient, date_patient, date_teste, nss, adresse_postale, telephone, e_mail):
        p = patient.Patient()
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        p.set_nss(nss)
        p.set_date_teste(date_teste)
        p.set_id_medecin(model_global.get_user_id())
        #Coordonnées du patient
        coord = p.get_coordonnees()
        coord.set_adresse_postale(adresse_postale)
        coord.set_telephone(telephone)
        coord.set_adresse_mail(e_mail)
        #Enregistrement et récupère l'id
        id = dao_patient.dao_Patient().insert_patient(p)
        #Recherche la personne dans la base
        pliste = dao_patient.dao_Patient().get_patient(id)
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Enregistrement d'un nouveau patient
        </legend>'''

        page = page + "<br>Nouveau patient <b>" + pliste.get_prenom() + " " + pliste.get_nom() + "</b> ajouté.<br>"
        page = page + "Votre patient peut désormais se connecter à l'aide des identifiants ci-dessous : <br>"
        page = page + super().get_acces_utilisateur(pliste.get_id_personne())
        page = page + '''
        <div><a href="liste_patients">Liste des patients</a>
        <a href="accueil_medecin">Accueil</a></div></fieldset>'''
        page = page + super().footer()
        return page
    enregistrer_patient.exposed = True

    #Affiche la liste des medecins dans la base
    def liste_patients(self, rechercher = ""):
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Les des patients
        </legend>
        <div>'''
        page = page + "<div><form action='liste_patients' method='GET'>"
        page = page + '<label for="rechercher">Recherche d\'un patient: </label>'
        page = page + '<input type="text" id="rechercher" name="rechercher" value="' + rechercher + '">'
        page = page + '<input  type="submit" value="Rechercher" class="button_vert">'
        page = page + "</form></div><div>"
        page = page + "<br><a href='ajouter_patient'> Ajouter un patient</a>"
        liste = dao_patient.dao_Patient().get_patients_medecin(model_global.get_user_id(), rechercher)
        page = page + "<table>"
        count = 1
        for c in liste :
            if count % 2 == 0:
                page = page + '<tr>'
            else :
                page = page + "<tr class='ligne_gris'>"
            page = page + '<td>' + c.get_nom() + " " +c.get_prenom()+'</td><td>'+ str(c.get_nss()) +'</td><td> <a href="suivi_patient?id=' + str(c.get_id())+'">Suivi</a></td></tr>'
            count = count + 1 
        page = page + "</table>"
        page = page + "</div></div></fieldset>"
        page = page + '<a href="accueil_medecin">Retour accueil</a>'
        page = page + super().footer()
        return page
    liste_patients.exposed = True

    #Suivie de patient
    def suivi_patient(self, id=-1, rubrique = 0) :
        self.patient_selected = dao_patient.dao_Patient().get_patient(id)
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Suivi de : <b>''' + self.patient_selected.get_prenom() + " " + self.patient_selected.get_nom()+ " - " + str(self.patient_selected.get_nss()) + "<b>"
        page = page + '''</legend>
        <div>'''
        page = page + '''<div class="liste_questions">
                    <div class="rubriques">'''
        #Parametres
        if int(rubrique) == 0:
            page = page + '''<div class="button_selected"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=0">Paramêtres</a></div>'''
        else :
            page = page + '''<div class="button"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=0">Paramêtres</a></div>'''
        #Frequents
        if int(rubrique) == 1:
            page = page + '''<div class="button_selected"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=1">Symptômes fréquents</a></div>'''
        else :
            page = page + '''<div class="button"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=1">Symptômes fréquents</a></div>'''
        #Moins Frequents
        if int(rubrique) == 2:
            page = page + '''<div class="button_selected"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=2">Symptômes moins fréquents</a></div>'''
        else :
            page = page + '''<div class="button"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=2">Symptômes moins fréquents</a></div>'''
        #Graves
        if int(rubrique) == 3:
            page = page + '''<div class="button_selected"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=3">Symptômes graves</a></div>'''
        else :
            page = page + '''<div class="button"><a href="suivi_patient?id=''' + str(id) + '''&rubrique=3">Symptômes graves</a></div>'''

        page = page + "</div>"
        page = page + "<table>"
        page = page + "<tr>"
        page = page + "<th>&nbsp;</th>"

        #Creation des colonnes
        liste_questions = dao_question.dao_Question().get_questions_niveau(rubrique)
        for quest in liste_questions:
            page = page + "<th>" + quest.get_intitule() + "</th>"
        page = page + "<th>Etat</th>"
        page = page + "</tr>"

        #Création des lignes
        questionnaires = dao_questionnaire.dao_Questionnaire().get_questionnaires_patient(self.patient_selected.get_id(), rubrique)
        count = 2
        indic = 0
        for q in questionnaires :
            if count % 2 == 0 :
                page = page + "<tr class='ligne_gris'>"
            else:
                page = page + "<tr>"

            page = page + "<td><a href='analyse_questionnaire_patient?id=" + str(q.get_id()) + "'>" + q.get_date() + "</a></td>"
            #les réponses
            indic = 0
            comp = None
            curr_quest = None
            niv_alerte = None
            type_q = None
            reponses = dao_reponse.dao_Reponse().get_reponses_questionnaire(q.get_id(), rubrique)
            for rep in reponses :
                print("Reponse:"+rep.to_string())
                curr_quest = liste_questions[indic]
                comp = curr_quest.get_comparateur()
                niv_alerte = curr_quest.get_reponse_alerte()
                type_q = curr_quest.get_type_reponse()
                if niv_alerte == None :
                    page = page + '<td>'
                else:
                    #Si reponse numérique
                    if type_q == "Numérique" :
                        print("Question Numérique")
                        val = float(rep.get_reponse())
                        niv_alerte = float(niv_alerte)
                        #Si comparateur : =
                        if comp == 2:
                            if val == niv_alerte :
                                page = page + '<td class="rep_alerte">'
                            else :
                                page = page + '<td>'
                        #Si comparateur : >
                        elif comp == 0:
                            if val > niv_alerte :
                                page = page + '<td class="rep_alerte">'
                            else :
                                page = page + '<td>'
                        #Si comparateur : >
                        elif comp == 1:
                            if val < niv_alerte :
                                page = page + '<td class="rep_alerte">'
                            else :
                                page = page + '<td>'
                    #Si reponse Textuelle
                    else:
                        print("Question Textuelle :"+rep.get_reponse() +"; alerte:"+niv_alerte)
                        if rep.get_reponse() == niv_alerte :
                            page = page + '<td class="rep_alerte">'
                        else :
                            page = page + '<td>'

                page = page + str(rep.get_reponse()) + "</td>"
                indic = indic + 1 
            print("Etat patient="+str(q.get_etat_patient()))
            if q.get_etat_patient() == -1:
                page = page + "<td class='etat_non_analyse'>&nbsp;</td>"
            elif q.get_etat_patient() == 0:
                page = page + "<td class='etat_gerrie'>&nbsp;</td>"
            elif q.get_etat_patient() == 1:
                page = page + "<td class='etat_moyen'>&nbsp;</td>"
            elif q.get_etat_patient() == 2:
                page = page + "<td class='etat_grave'>&nbsp;</td>"
            elif q.get_etat_patient() == 3:
                page = page + "<td class='etat_tres_grave'>&nbsp;</td>"
            elif q.get_etat_patient() == 4:
                page = page + "<td class='etat_decede'>&nbsp;</td>"
            page = page + "</tr>"
            count = count + 1

        page = page + "</table>"
        page = page + "</div>"
        page = page + "</fieldset>"
        page = page + '<a href="liste_patients">Retour liste des patients</a>'
        page = page + "<div class='infos_patient'>"
        page = page + self.infos_patient(id)
        page = page + "</div>"
        page = page + super().footer()
        return page
    suivi_patient.exposed = True


    #Liste des questionnaires non analysés
    def questionnaires_non_analyses(self):
        page = super().entete()
        page = page + '''<fieldset class="cadre">
        <legend>
            Questionnaires non analysés
        </legend>
        <div>'''
        liste = dao_patient.dao_Patient().get_patients_medecin_non_analyses(model_global.get_user_id())
        page = page + "<table>"
        count = 1
        for c in liste :
            if count % 2 == 0:
                page = page + '<tr>'
            else :
                page = page + "<tr class='ligne_gris'>"
            page = page + '<td>' + c.get_nom() + " " +c.get_prenom()+'</td><td>'+ str(c.get_nss()) +'</td><td> <a href="suivi_patient?id=' + str(c.get_id())+'">Suivi</a></td></tr>'
            count = count + 1 
        page = page + "</table>"
        page = page + "</div></fieldset>"
        page = page + super().footer()
        return page
    questionnaires_non_analyses.exposed = True

    def infos_patient(self, id):
        p = dao_patient.dao_Patient().get_patient(id)
        page = super().entete()
        page = page + '''<fieldset class="cadre">
        <legend>
            Informations patient
        </legend>
        <div>'''
        page = page + p.get_prenom() + " " + p.get_nom() + "<br>"
        if not (p.get_coordonnees() == None) :
            coord = p.get_coordonnees()
            page = page +  coord.get_adresse_postale() + "<br>"
            page = page + "E-mail: " + coord.get_adresse_mail() + "<br>"
            page = page + "Tel: " + coord.get_telephone() + "<br>"
        page = page + "</div></fieldset>"
        return page
    infos_patient.exposed = True


    def ligne_reponse(self, niveau, questionnaire):
        liste_questions = dao_question.dao_Question().get_questions_niveau(niveau)
        count = 2
        page = ""
        rep = ""
        page = page +"taille reps:"+ str(len(questionnaire.get_reponses()))
        for quest in liste_questions:
            for r in questionnaire.get_reponses():
                if int(quest.get_id()) == int(r.get_id_question()) :
                    rep = r.get_reponse()
                    break
                else :
                    rep = str(quest.get_id())+"-"+str(r.get_id_question())

            if count%2 == 0:
                page = page + "<tr><td><b>" + quest.get_intitule() + "</b><br>" + quest.get_description() + "</td><td>" + str(rep) + "</td></tr>"
            else :
                page = page + "<tr class='ligne_gris'><td><b>" + quest.get_intitule() + "</b><br>" + quest.get_description() + "</td><td>" + str(rep) + "</td></tr>"

            count = count + 1
        return page

    def analyse_questionnaire_patient(self, id):
        page = super().header()
        quest = dao_questionnaire.dao_Questionnaire().get_questionnaire(id)
        page = page + '''<fieldset class="cadre">
                        <legend>
            Suivi de : <b>''' + self.patient_selected.get_prenom() + " " + self.patient_selected.get_nom()+ " - " + str(self.patient_selected.get_nss())
        page = page + '''</legend>'''
        page = page + '<div><table>'

        #Parametres
        page = page + "<tr><td colspan=2 class='cel_titre_ribrique'><b>Questionnaire du : " + quest.get_date() + "</b></td></tr>"
        page = page + "<tr><td colspan=2 class='cel_titre_ribrique'>Paramêtres</td></tr>"
        page = page + self.ligne_reponse(0, quest)

        #Frequents
        page = page + "<tr><td colspan=2 class='cel_titre_ribrique'>Symptômes fréquents</td></tr>"
        page = page + self.ligne_reponse(1, quest)

        #Moins frequents
        page = page + "<tr><td colspan=2 class='cel_titre_ribrique'>Symptômes moins fréquents</td></tr>"
        page = page + self.ligne_reponse(2, quest)

        #Graves
        page = page + "<tr><td colspan=2 class='cel_titre_ribrique'>Symptômes graves</td></tr>"
        page = page + self.ligne_reponse(3, quest)


        page = page + "</table>"
        page = page + "</div>"

        page = page + "</fieldset>"
        page = page + '<fieldset ><legend>Commentaire</legend><div>'
        page = page + quest.get_commentaire()
        page = page + "</div></fieldset>"

        page = page + '<fieldset ><legend>Analyse</legend><div>'
        page = page + "<form action='enregistrer_analyse' method='GET'>"
        page = page + '<input type="hidden" name="id" value="' + str(id) + '">'
        page = page + '<div class="conteneur_analyse"><div class="text_analyse"><textarea id="reponse" name="analyse" rows="8" cols="50" >' +  quest.get_analyse() + '</textarea></div>'
        page = page + '''<div class="radio_etat">
                            <div><input type="radio" id="non_analyse" name="etat_patient" value=-1 checked>
                            <label for="non_analyse" >Non analysé</label></div>

                            <div><input type="radio" id="gerrie" name="etat_patient" value=0>
                            <label for="gerrie" class="couleur_gerrie">Guéris</label></div>

                            <div class="couleur_moyen"><input type="radio" id="moyen" name="etat_patient" value=1>
                            <label for="moyen">Moyen</label></div>

                            <div class="couleur_grave"><input type="radio" id="grave" name="etat_patient" value=2>
                            <label for="grave">Grave</label></div>

                            <div class="couleur_tres_grave"><input type="radio" id="tres_grave" name="etat_patient" value=3>
                            <label for="tres_grave">Très grave</label></div>

                            <div><input type="radio" id="decede" name="etat_patient" value=4>
                            <label for="decede" class="couleur_decede">Décèdé</label></div>

                        </div>
                        <div><input type="submit" value="Valider" class="button_vert"></div></div>'''
        page = page + "</form>"
        page = page + "</div></fieldset>"
        page = page + super().footer()
        return page
    analyse_questionnaire_patient.exposed = True

    def enregistrer_analyse(self, id, analyse, etat_patient) :
        dao_questionnaire.dao_Questionnaire().update_questionnaire2(id, analyse, etat_patient)
        page = super().header()
        page = page + '<fieldset ><legend>Confirmation enregistrement</legend>'
        page = page + "Analyse enregistrée.<br><a href='suivi_patient?id=" + str(self.patient_selected.get_id()) + "'>Retour</a>"
        page = page + "</div></fieldset>"
        page = page + super().footer()
        return page
    enregistrer_analyse.exposed = True


    def liste_questions(self):
        if int(self.rubrique) == 0:
            page = self.questions_parametres()
        if int(self.rubrique) == 1:
            page = self.questions_sympt_frequents()
        if int(self.rubrique) == 2:
            page = self.questions_sympt_moins_frequents()
        if int(self.rubrique) == 3:
            page = self.questions_sympt_graves()
        return page
    liste_questions.exposed = True

    def questions_sympt_graves(self, rubrique = 3):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Symptômes graves
        </legend>'''
        page = page + '''<div>
                    <div class="rubriques">
                        <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                        <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                        <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                        <div class="button_selected"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
                    </div>
                    <div class="liste_questions">'''

        #Parametres du patients
        page = page + "<div><a href='nouveau_question?niveau=3'>Ajouter une question</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(3)
        for c in liste :
            page = page + '<li>' + c.to_string() +"</li>"
        page = page + '''</ol></div></div></div></fieldset>
        <a href="accueil_medecin">Retour accueil</a>'''
        page = page + super().footer()
        return page
    questions_sympt_graves.exposed = True

    def questions_sympt_moins_frequents(self, rubrique = 2):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Symptômes moins fréquents
        </legend>'''
        page = page + '''<div>
                    <div class="rubriques">
                        <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                        <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                        <div class="button_selected"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                        <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
                    </div>
                    <div class="liste_questions">'''

        #Parametres du patients
        page = page + "<div><a href='nouveau_question?niveau=2'>Ajouter une question</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(2)
        for c in liste :
            page = page + '<li>' + c.to_string() +"</li>"
        page = page + '''</ol></div></div></div></fieldset>
        <a href="accueil_medecin">Retour accueil</a>'''
        page = page + super().footer()
        return page
    questions_sympt_moins_frequents.exposed = True

    def questions_sympt_frequents(self, rubrique = 1):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Symptômes fréquents
        </legend>'''
        page = page + '''<div>
                    <div class="rubriques">
                        <div class="button"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                        <div class="button_selected"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                        <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                        <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
                    </div>
                    <div class="liste_questions">'''

        #Parametres du patients
        page = page + "<div><a href='nouveau_question?niveau=1'>Ajouter une question</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(1)
        for c in liste :
            page = page + '<li>' + c.to_string() +"</li>"
        page = page + '''</ol></div></div></div></fieldset>
        <a href="accueil_medecin">Retour accueil</a>'''
        page = page + super().footer()
        return page
    questions_sympt_frequents.exposed = True

    def questions_parametres(self, rubrique = 0):
        self.rubrique = rubrique
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Paramêtres
        </legend>'''
        page = page + '''<div>
                    <div class="rubriques">
                        <div class="button_selected"><a href="questions_parametres?rubrique=0">Paramêtres</a></div>
                        <div class="button"><a href="questions_sympt_frequents?rubrique=1">Symptômes fréquents</a></div>
                        <div class="button"><a href="questions_sympt_moins_frequents?rubrique=2">Symptômes moins fréquents</a></div>
                        <div class="button"><a href="questions_sympt_graves?rubrique=3">Symptômes graves</a></div>
                    </div>
                    <div class="liste_questions">'''
        #Parametres du patients
        page = page + "<div><a href='nouveau_question?niveau=0'>Ajouter une question</a>"
        page = page + "<ol>"
        liste = dao_question.dao_Question().get_questions_niveau(0)
        count = 1 
        for c in liste :
            if count % 2 == 0:
                page = page + '<li class="ligne_gris">' + c.to_string() +"</li>"
            else :
                page = page + '<li>' + c.to_string() +"</li>"
            count = count + 1 
        page = page + '''</ol></div></div></div></fieldset>
        <a href="accueil_medecin">Retour accueil</a>'''
        page = page + super().footer()
        return page
    questions_parametres.exposed = True

    def nouveau_question(self, niveau):
        page = super().header()
        page = page + '''<fieldset class="cadre">
        <legend>
            Ajouter une question
        </legend>'''
        page = page + '''
        <form action="enregistrer_question" method="GET">
            <div>
            <label for="niveau">Niveau :</label>
                <select name="niveau" id="niveau">'''
        if int(self.rubrique) == 0 :
            page = page + "<option value=0 selected >Paramêtres</option>"
        else :
            page = page + "<option value=0>Paramêtres</option>"

        if int(self.rubrique) == 1 :
            page = page + "<option value=1 selected >Fréquent</option>"
        else :
            page = page + "<option value=1>Fréquent</option>"

        if int(self.rubrique) == 2 :
            page = page + "<option value=2 selected > Moins fréquent</option>"
        else :
            page = page + "<option value=2>Moins fréquent</option>"

        if int(self.rubrique) == 3 :
            page = page + "<option value=3 selected >Grave</option>"
        else :
            page = page + "<option value=3>Grave</option>"

        page = page + '''</select><br>
                <label for="intitule">Intitulé:</label><br>
                <textarea id="intitule" name="intitule" rows="2" cols="50"></textarea><br>

                <label for="description">Déscription:</label><br>
                <textarea id="description" name="description" rows="4" cols="50"></textarea><br>
                
                <label for="type_reponse">Type de réponse :</label>
                <select name="type_reponse" id="type_reponse">
                    <option value="Texte" selected >Texte</option>
                    <option value="Numérique" selected >Numérique</option>
                </select><br>
                
                <label for="valeur">Réponse par défaut:</label><br>
                <textarea id="valeur" name="valeur" rows="2" cols="50"></textarea><br>

                <label for="reponse_alerte">Réponse alerte:</label><br>
                <input type="text" id="reponse_alerte" name="reponse_alerte">
                <select name="comparateur" id="comparateur">
                    <option value=0 >Plus grand</option>
                    <option value=1 >Plus petit</option>
                    <option value=2 selected>Egale</option>
                </select>
                <input type="submit" value="Enregistrer">
            </div>
        </form>
        </fieldset>'''
        page = page + super().footer()
        return page
    nouveau_question.exposed = True


    def enregistrer_question(self, niveau, intitule, description, valeur, type_reponse, reponse_alerte, comparateur):
        dao_question.dao_Question().insert_question2(intitule, description, valeur, niveau, type_reponse, reponse_alerte, comparateur)
        self.rubrique = niveau
        return self.liste_questions()
    enregistrer_question.exposed = True