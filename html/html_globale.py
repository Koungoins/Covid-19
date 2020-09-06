#!/bin/env python
# coding=utf-8

#import cherrypy
import model_global

class Page_Globale(object) :


    def get_css(self):
        page = '''
body {
    /*background: url(white-sand.png);*/
    /*background-color : light-grey;*/
}

.entete_connexion {
	width: 300px;
	float:right;
}

.box {
    width: 600px;
	margin: 0 auto;
    background-color: white;
    border-radius: 30%;
}

.connexion{
	width: 300px;
    float:center;
}

.accueil {
    width: 300px;
}

fieldset {
    background-color: #ffffff;
    margin: 0 auto 15px auto;
    padding: 10px;
    border: 2px solid #eeab69;
    -moz-border-radius: 20px;
    -webkit-border-radius: 10px;
    border-radius: 10px;
    behavior: url(border-radius.htc);

    background-image: -moz-linear-gradient(top, #ffffff, #f4f4f4);
    background-image: -webkit-gradient(linear, left top, left bottom, from(#ffffff), to(#f4f4f4));
    filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#f4f4f4);
    -ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr=#ffffff,endColorstr=#f4f4f4)";
}

legend {
    color: #eeab69;
}

.cadre {
	margin-top: 100px;
}

.rubriques {
	width: 550px;
    height: 70px;
	float: center;
}

.bouton_bas {
    width: 550px;
    float:center;
    height: 50px;
}


.liste_questions {
	width: 550px;
	float:center;
}

.liste_questions img {
	width: 20px;
}

.button_vert {
    width: 200px;
    height: 40px;
	float:center;
    background: linear-gradient(to bottom, #edeef3ea 0%,#ffffff 100%);
    border: none;
    border-radius: 5px;
    position: relative;
    border-bottom: 4px solid #bfd2df;
    color: #fbfbfb;
    font-weight: 600;
    font-family: 'Open Sans', sans-serif;
    text-shadow: 1px 1px 1px rgba(0,0,0,.4);
    font-size: 15px;
    text-align: center;
    text-indent: 5px;
    box-shadow: 0px 3px 0px 0px rgba(0,0,0,.2);
    cursor: pointer;

    display: auto;
    margin: 0 auto;
    margin-top: 10px;
  }

.button_suiv {
    width: 200px;
    height: 40px;
	float:right;
    background: linear-gradient(to bottom, #edeef3ea 0%,#ffffff 100%);
    border: none;
    border-radius: 5px;
    position: relative;
    border-bottom: 4px solid #bfd2df;
    color: #fbfbfb;
    font-weight: 600;
    font-family: 'Open Sans', sans-serif;
    text-shadow: 1px 1px 1px rgba(0,0,0,.4);
    font-size: 15px;
    text-align: center;
    text-indent: 5px;
    box-shadow: 0px 3px 0px 0px rgba(0,0,0,.2);
    cursor: pointer;

    display: auto;
    margin: 0 auto;
  }

  .button_preced {
    width: 200px;
    height: 40px;
	float:left;
    background: linear-gradient(to bottom, #edeef3ea 0%,#ffffff 100%);
    border: none;
    border-radius: 5px;
    position: relative;
    border-bottom: 4px solid #bfd2df;
    color: #fbfbfb;
    font-weight: 600;
    font-family: 'Open Sans', sans-serif;
    text-shadow: 1px 1px 1px rgba(0,0,0,.4);
    font-size: 15px;
    text-align: center;
    text-indent: 5px;
    box-shadow: 0px 3px 0px 0px rgba(0,0,0,.2);
    cursor: pointer;

    display: auto;
    margin: 0 auto;
  }

.rubriques .button {
    width: 130px;
    height: 40px;
	float:left;
    background: linear-gradient(to bottom, #edeef3ea 0%,#ffffff 100%);
    border: none;
    border-radius: 5px;
    position: relative;
    /*border-bottom: 4px solid #bfd2df;*/
    color: #fbfbfb;
    font-weight: 600;
    font-family: 'Open Sans', sans-serif;
    /*text-shadow: 1px 1px 1px rgba(0,0,0,.4);*/
    font-size: 15px;
    text-align: center;
    text-indent: 5px;
    box-shadow: 0px 3px 0px 0px rgba(0,0,0,.2);
    cursor: pointer;

    display: auto;
    margin-left: 3px;
  }

.rubriques .button_selected {
    width: 130px;
    height: 40px;
	float:left;
    background: linear-gradient(to bottom, #edeef3ea 0%,#ffffff 100%);
    border: none;
    border-radius: 5px;
    position: relative;
    border-bottom: 4px solid #eb4908;
    color: #fbfbfb;
    font-weight: 600;
    font-family: 'Open Sans', sans-serif;
    /*text-shadow: 1px 1px 1px rgba(0,0,0,.4);*/
    font-size: 15px;
    text-align: center;
    text-indent: 5px;
    box-shadow: 0px 3px 0px 0px rgba(0,0,0,.2);
    cursor: pointer;

    display: auto;
    margin-left: 3px;
  }'''

        return page

    def entete(self) :
        #'<link href="/annexes/css.css" rel="stylesheet">'
        return '''<html>
		  <head>
            <style type="text/css">'''+self.get_css()+'''</style>
		  </head><body><div>'''

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
            page = page + '''<div><form action="deconnexion" methode="GET">
                    <input type="submit" value="Déconnexion">
                </form></div>'''

        page = page +  '''</div>
        <div class="box">'''
        return page

    def footer(self):
        return '</div></body></html>'

    #Identification d'un patient
    def connexion(self, titre):
        page = self.entete()
        page = page + "<div class='box'>"
        page = page + '''<fieldset class="cadre">
        <legend>
            Connexion
        </legend>'''
        page = page + "<div>"
        page = page + '''<div><form action="verif_connexion" methode="GET">
                    <label for="login">Identifiant :</label>
                    <input type="text" id="login" name="login"><br>
                    <label for="passe">Mot de passe :</label>
                    <input type="password" id="passe" name="passe"><br>
                    <input type="submit" value="Connexion">
                </form>
            </div>
        </div></fieldset></div>
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