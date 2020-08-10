#!/bin/env python
# coding=utf-8
import threading as thread
import SQLiteManager as db
import os.path
import cherrypy

#Classes base de données
from dao import dao_Personne
from dao import dao_Acces
from dao import dao_Coordonnees

#Classes métier
from objects import Personne
from objects import Acces
from objects import Coordonnees

#classes html
from html import html_Personne


class Accueil(object):
    @cherrypy.expose
    def index(self):
        page = ''' <h1>Page d'accueil</h1>
        <a href="/personne/">Liste des personnes</a>
        '''
        return page

#Definition des liens vers les classes
root = Accueil()
#lien vers la classse html_Personne : /personne/
root.personne = html_Personne.html_Personne()

config_serveur = os.path.join(os.path.dirname(__file__), 'serveur_web.conf')
cherrypy.quickstart(root, config = config_serveur)