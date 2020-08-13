#!/bin/env python
# coding=utf-8
import cherrypy

from dao import dao_patient
from dao import dao_personne
from objects import patient
from objects import personne
from html import html_globale
import model_global


#class Page_ConnexionPatient(html_connexion.Page_Connexion):

class Pages_Patients(html_globale.Page_Globale) :

    def __init__(self):
        self.titre_page = "Espace patients"

    def index(self):
        return self.connexion("Espace patients")
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
            page = super().header()
            page = page + "Bonjour " + pers.get_nom() + " " + pers.get_prenom()
            page = page + "<br>Vous êtes connecté !"
            page = page + super().footer()
            return page
    verif_connexion.exposed = True

    #Formulaire pour ajouter un patient
    def ajouter(self):
        page = '''
        <title>Créer un nouveau patient</title>
        <h1>Créer un nouveau patient</h1>
        <form action="enregistrer" method="GET">
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
        return page
    ajouter.exposed = True


    #Affiche la liste des medecins dans la base
    def liste(self):
        page = "Les des patients : <a href='ajouter'> Ajouter</a>"
        liste = dao_patient.dao_Patient().get_all_patients()
        for c in liste :
            #page = page + "<br><a href='edit?id="+str(c.get_id())+">"+c.to_string()+"</a>"
            page = page + '<br>' + c.to_string() + '<a href="edit?id=' + str(c.get_id())+'">Editer</a>'
        return page
    liste.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer(self, nom_patient, prenom_patient, date_patient, nss):
        p = patient.Patient()
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        p.set_nss(nss)
        #Enregistrement et récupère l'id
        id = dao_patient.dao_Patient().insert_patient(p)
        #Recherche la personne dans la base
        pliste = dao_patient.dao_Patient().get_patient(id)
        page ="Nouveau patient : <br>"
        page = page + pliste.to_string()
        page = page + '''
        <form action="liste"><input type="submit" value="Liste des patients"></form>
        '''
        return page
    enregistrer.exposed = True

    #Formulaire permettant de modifier les infos d'une personne
    def edit(self, id):
        self.id_edite = id
        page = "<h1>Edition d'une personne</h1>"
        p = dao_patient.dao_Patient().get_patient(id)
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
                <input type="number" id="nss" name="nss" value="'''+p.get_nss()+ '''"><br>
                <input type="submit" value="Modifier">
            </div>
        </form>
        '''
        return page
    edit.exposed = True

    #Met à jour les infos d'edition dans la base
    def update(self, nom_patient, prenom_patient, date_patient):
        p = personne.Personne()
        p.set_id(self.id_edite)
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        #Enregistrement et récupère l'id
        dao_personne.dao_Personne().update_personne(p)
        #Recherche la personne dans la base
        pliste = dao_personne.dao_Personne().get_personne(self.id_edite)
        page = pliste.to_string()
        return page
    update.exposed = True

    #Supprime la personne dans la base
    def supprimer(self, id):
        dao_personne.dao_Personne().delete_personne2(id)
        page = "Personne supprimée.<br>"
        page = page + self.liste()
        return page
    supprimer.exposed = True
