#!/bin/env python
# coding=utf-8

import cherrypy

user_connected = "user_connected"
user_type = "type_user"
user_type_patient = "patients"
user_type_medecin = "medecins"
user_id = "id_user"
user_id_personne = "id_personne_user"
user_nom = "nom_user"
user_prenom = "prenom_user"


def connect_user(type, id, nom, prenom, id_personne):
    print("Connecté : id="+str(id)+", nom="+nom+", prenom="+prenom+", id_personne="+str(id_personne))
    cherrypy.session[user_connected] = True
    cherrypy.session[user_type] = type
    cherrypy.session[user_id] = id
    cherrypy.session[user_nom] = nom
    cherrypy.session[user_prenom] = prenom
    cherrypy.session[user_id_personne] = id_personne

def deconnect_user():
    cherrypy.session[user_connected] = False
    cherrypy.session[user_type] = None
    cherrypy.session[user_id] = None
    cherrypy.session[user_nom] = None
    cherrypy.session[user_prenom] = None
    cherrypy.session[user_id_personne] = None

def get_user_type():
    return cherrypy.session.get(user_type, None)

def get_user_id():
    return cherrypy.session.get(user_id, None)

def get_user_nom():
    return cherrypy.session.get(user_nom, None)

def get_user_prenom():
    return cherrypy.session.get(user_prenom, None)

def get_user_id_personne():
    return cherrypy.session.get(user_id_personne, None)

def is_user_connected():
    return cherrypy.session.get(user_connected, False)