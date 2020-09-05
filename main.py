#!/bin/env python
# coding=utf-8
import threading as thread
import SQLiteManager as db
import os, os.path
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
from html import html_globale
from html import html_questions

class Accueil(html_globale.Page_Globale):

    def index(self):
        yield html_globale.Page_Globale().header()
        yield ''' <h1>Page d'accueil</h1>
        <div>
            <div><a href="/patients/">Espace patients</a></div>
            <div><a href="/medecins/">Espace médecins</a></div>
        </div>
        '''
        yield super().footer()

    index.exposed = True


#Definition des liens vers les classes
root = Accueil()

#lien vers les pages dans les classes
root.patients = html_patients.Pages_Patients()
root.medecins = html_medecins.Pages_Medecins()
#root.questions = html_questions.Pages_Questions()
root.accueil = Accueil()

config_serveur = os.path.join(os.path.dirname(__file__), 'serveur_web.conf')

if __name__ == '__main__' :
    config = {
        'global' : {
            'server.socket_host' : '127.0.0.1',
            'server.socket_port' : 8080,
            'server.thread_pool' : 10
        },
		'/': {
		 'tools.sessions.on': True,
		 'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/annexes': {
		 'tools.staticdir.on': True,
		 'tools.staticdir.dir': './public'
		}
	}
    #db.SQLiteManager().init_data_base()
    cherrypy.quickstart(root, '/', config)

