#!/bin/env python
# coding=utf-8

import cherrypy
import model_global

class Page_Globale(object) :


    def entete(self) :
        return '''<html>
		  <head>
			<link href="./annexes/css.css" rel="stylesheet">
		  </head><body>'''

    def header(self):
        page = self.entete()
        page =  page + '''<div class="entete_connexion">'''
        if not model_global.is_user_connected() :
           # page = page + '''<div><form action="connexion" methode="GET">
            #        <input type="submit" value="Connexion">
             #   </form>
            #</div>'''
            page = ""
        else :
            page = page + str(model_global.get_user_id())  +" Bonjour " + model_global.get_user_nom() + " " + model_global.get_user_prenom()
            page = page +  '''<div><form action="deconnexion" methode="GET">
                    <input type="submit" value="Déconnexion">
                </form></div>'''

        page = page +  '''</div>
        <div class="box">'''
        return page

    def footer(self):
        return '</div></body></html>'

    #Identification d'un patient
    def connexion(self, titre):
        page = self.header()
        page = page + "<div><h1>" + titre + "</h1>"
        page = page + '''<div><form action="verif_connexion" methode="GET">
                    <label for="login">Identifiant :</label>
                    <input type="text" id="login" name="login"><br>
                    <label for="passe">Mot de passe :</label>
                    <input type="password" id="passe" name="passe"><br>
                    <input type="submit" value="Connexion">
                </form>
            </div>
        </div>
        '''
        page = page + self.footer()
        return page
    connexion.exposed = True

    def deconnexion(self) :
        model_global.deconnect_user()
        return self.vers_accueil()
    deconnexion.exposed = True

    def vers_accueil(self):
        return '<head><meta http-equiv="refresh" content="0;URL=/accueil/"></head>'
    deconnexion.exposed = True