#!/bin/env python
# coding=utf-8
from dao import dao_personne
from dao import dao_medecin
from objects import medecin
from objects import personne
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
        <li><a href="nouveau_medecin">Nouveau médecin</a></li>
        <li><a href="liste_medecins">Liste des médecins</a></li>
        <li><a href="ajouter">Nouveau médecin</a></li>
        </ul>'''
        page = page + super().footer()
        return page
    accueil_medecin.exposed = True

    #Formulaire pour ajouter un médecin
    def nouveau_medecin(self):
        page = '''
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
        return page
    nouveau_medecin.exposed = True


    #Affiche la liste des medecins dans la base
    def liste_medecins(self):
        page = "Les des médecins : <a href='nouveau_medecin'>Ajouter</a>"
        liste = dao_medecin.dao_Medecin().get_all_medecins()
        for c in liste :
            #pers = c[1]
            page = page + '<br>' + c.to_string() + ' <a href="edit?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a>'
        return page
    liste_medecins.exposed = True

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    def enregistrer_medecin(self, nom = "", prenom = "", daten = "", rpps = -1, liberal = False, hopital = ""):
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
        #Enregistrement et récupère l'id
        id = dao_medecin.dao_Medecin().insert_medecin(p)
        #Recherche la personne dans la base
        pliste = dao_medecin.dao_Medecin().get_medecin(id)
        page ="Nouvelle personne : <br>"
        page = page + pliste.to_string()
        page = page + '''
        <form action="liste_medecins"><input type="submit" value="Liste des personnes"></form>
        '''
        return page
    enregistrer_medecin.exposed = True

    #Formulaire permettant de modifier les infos d'une personne
    def edit(self, id):
        self.id_edite = id
        page = "<h1>Edition d'un médecin</h1>"
        p = dao_medecin.dao_Medecin().get_medecin(id)
        page = page + '''
        <form action="update" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom_patient" value="'''+p.get_nom()+ '''"><br>
                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom_patient" value="'''+p.get_prenom()+ '''"><br>
                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="date_patient" value="'''+p.get_date_de_naiss()+ '''"><br>
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
        page = page + self.liste_medecins()
        return page
    supprimer.exposed = True
