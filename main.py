#!/bin/env python
# coding=utf-8
import threading as thread
import SQLiteManager as db
#from cherrypy import cherrypy
import os.path
from dao import dao_Personne
from dao import dao_Acces
from dao import dao_Coordonnees



class MonSiteWeb(object):

    def index(self):
        return "<h1>Bonjour à tous !</h1>"
    #index.exposed = True

#config_serveur = os.path.join(os.path.dirname(__file__), 'serveur_web.conf')
#cherrypy.quickstart(MonSiteWeb(), config = config_serveur)

manager = db.SQLiteManager()
manager.init_data_base()
#dao_Personne.dao_Personne().insert_personne2(3, "BINA", "Aouda", 19841008)
#dao_Acces.dao_Acces().insert_acces2(1, "login1", "mot de passe 1", 3)
#dao_Acces.dao_Acces().insert_acces2(2, "login1", "mot de passe 1", 1)


#dao_Personne.dao_Personne().update_personne2(3,'HALADI', 'Bina', 19850201)

liste = dao_Personne.dao_Personne().get_personne(2)
print(liste.to_string())

liste = dao_Personne.dao_Personne().get_all()
for c in liste :
    print(c.to_string())

liste = dao_Acces.dao_Acces().get_acces(2)

print(liste.to_string())