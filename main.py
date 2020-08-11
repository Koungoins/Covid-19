#!/bin/env python
# coding=utf-8
import threading as thread
import SQLiteManager as db
import os.path
import cherrypy

#Classes base de données
from dao import dao_personne
from dao import dao_acces
from dao import dao_coordonnees
from dao import dao_medecin

#Classes métier
from objects import personne
from objects import acces
from objects import coordonnees
from objects import medecin

#classes html
from html import html_medecins
from html import html_patients

class Accueil(object) :

    @cherrypy.expose
    def index(self):
        page = ''' <h1>Page d'accueil</h1>
        <a href="/medecins/">Liste des médecins</a><br>
        <a href="/patients/">Liste des patients</a><br>
        '''
        return page

#Definition des liens vers les classes
root = Accueil()
#lien vers les pages dans les classes
root.medecins = html_medecins.Pages_Medecins()
root.patients = html_patients.Pages_Patients()

config_serveur = os.path.join(os.path.dirname(__file__), 'serveur_web.conf')



if __name__ == '__main__' :
    #db.SQLiteManager().init_data_base()
    cherrypy.quickstart(root, config = config_serveur)


#med = medecin.Medecin()
#med.set_nom("CHEVALIER")
#med.set_prenom("Jean Pierre")
#med.set_date_de_naiss('1965-05-25')
#med.set_liberal(False)
#med.set_hopital("CHM Mamoudzou")
#id = dao_medecin.dao_Medecin().insert_medecin(med)
#print("Nouveau:"+str(id))

coord = coordonnees.Coordonnees()
coord.set_adresse_mail("mail@gmail.com")
coord.set_telephone("0125368541")
coord.set_adresse_postale("Mayotte")
coord.set_id_personne(52)
#id = dao_coordonnees.dao_Coordonnees().insert_coordonnees(coord)
#id = dao_coordonnees.dao_Coordonnees().insert_coordonnees2(coord.get_telephone(), coord.get_adresse_postale(), coord.get_adresse_mail(), coord.get_id_personne())
#print("Nouveau:"+str(id))

acc = acces.Acces()
acc.set_login("perso")
acc.set_mot_de_passe("motdepasse")
acc.set_id_personne(17)
#id = dao_acces.dao_Acces().insert_acces(acc)
#print("Nouveau:"+str(id))