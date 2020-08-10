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

#Classes métier
from objects import personne
from objects import acces
from objects import coordonnees

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
    cherrypy.quickstart(root, config = config_serveur)