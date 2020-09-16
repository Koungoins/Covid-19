#!/bin/env python
# coding=utf-8

#import cherrypy
import model_global
import hashlib
from datetime import date
from time import gmtime, strftime
from datetime import timedelta
from dao import dao_patient
from dao import dao_personne
from dao import dao_questionnaire
from objects import personne
from dao import dao_acces
from objects import acces


class Page_html(object) :


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


table tr tt {
	transform:rotate(270deg);
    -ms-transform:rotate(270deg); /* Internet Explorer */
    -moz-transform:rotate(270deg); /* Firefox */
    -webkit-transform:rotate(270deg); /* Safari et Chrome */
    -o-transform:rotate(270deg); /* Opera */
}

.ligne_gris {
    background-color:#D8C9B8;
}

.cel_titre_ribrique {
    text-align: center;
    background-color: burlywood;
    padding: 10px;
}

legend {
    color: #eeab69;
}

.conteneur_analyse{
    width: 600px;
}

.text_analyse{
    margin: 0px;
    width: 450px;
    height: 138px;
    float: left;
}

.infos_patient {
    width: 800px;
    margin: auto;
}

.recap_nouveaux{
    color: black;
    font-size: larger;
}

.recap_gerrie{
    color: green;
    font-size: larger;
}

.recap_moyen {
    color: #FFE837;
    font-size: larger;
}

.recap_grave {
    color: orange;
    font-size: larger;
}

.recap_tres_grave {
    color: darkred;
    font-size: larger;
}

.recap_decede {
    color: grey;
    font-size: larger;
}

.couleur_gerrie {
    color: green;
}

.couleur_moyen {
    color: #FFE837;
}

.couleur_grave {
    color: orange;
}

.couleur_tres_grave {
    color: darkred;
}

.couleur_decede {
    color: grey;
}

.etat_non_analyse {
    background: white;
}

.etat_gerrie {
    background: green;
}

.etat_moyen {
    background: #FFE837;
}

.etat_grave {
    background: orange;
}

.etat_tres_grave {
    background: darkred;
}

.etat_decede {
    background: grey;
}

.conteneur_recap {
    width: 700px;
    float : left;
}

.div_etat_patient{
    width : 100px;
}

.case_recap {
    width: 300px;
    /*height: 300px;*/
    margin-right: 30px;
    float : left;
}

.radio_etat {
    width: 120px;
    float: left;
}

.cadre {
    width: 800px;
    margin: auto;
}

table {
    width: 800px;
}

.rubriques {
	width: 800px;
    height: 70px;
}

.bouton_bas {
    width: 800px;
    float:center;
    height: 50px;
    margin-top: 20px;
}

.titre {
    text-align: center;
    color: #eeab69;
}

.liste_questions {
	width: 800px;
	float:center;
}

.liste_questions img {
	width: 20px;
}

.navigation_pages{
    width: 10px;
    text-align: left;
    margin: auto;
}

.rep_alerte {
    color: red;
}

.button_vert {
    width: 200px;
    height: 40px;
	float:center;
    background: burlywood;
    border: none;
    border-radius: 5px;
    position: relative;
    /*border-bottom: 4px solid #bfd2df;*/
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
    background: burlywood;
    border: none;
    border-radius: 5px;
    position: relative;
    /*border-bottom: 4px solid #bfd2df;*/
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
    background: burlywood;
    border: none;
    border-radius: 5px;
    position: relative;
    /*border-bottom: 4px solid #bfd2df;*/
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
    background: burlywood ;
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
    background: linear-gradient(to bottom, burlywood  0%,burlywood  100%);
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
            page = page + ' <div style="color: burlywood; font-size: 20px;">Bonjour <b>' + model_global.get_user_nom() + ' ' + model_global.get_user_prenom()+'</b></div>'
            page = page + '''<div><form action="deconnexion" methode="GET">
                    <input type="submit" value="Déconnexion" class="button_vert">
                </form></div></div>'''

        page = page +  '''</div>
        '''
        return page

    def footer(self):
        return '</body></html>'

    #Page "Connexion"
    def connexion(self, titre, medecin=0):
        page = self.entete()
        page = page + '''<fieldset class="cadre">
        <legend>'''
        if medecin == 1 :
            page = page + "Connexion médecin"
        else :
            page = page + "Connexion patient"

        page = page + '''</legend>'''
        page = page + '''<div style="width: 200px; margin: auto;"><form action="verif_connexion" methode="GET">'''
        page = page + '''<label for="login">Identifiant :</label><br>
                    <input type="text" id="login" name="login"><br><br>
                    <label for="passe">Mot de passe :</label><br>
                    <input type="password" id="passe" name="passe"><br>
                    <div style="width: 200px; margin: auto;"> '''
        if medecin == 1 :
            page = page + '<a href="nouveau_medecin">S\'inscrire</a><br>'
        page = page + '<input type="submit" value="Connexion" class="button_vert"></div>'
        page = page + '''
                </form>
            </div>
        </fieldset></div>
        '''
        page = page + self.footer()
        return page
    connexion.exposed = True

    #Page  "Covid-19 en temps réel"
    def tableau_chiffres(self):
        #Aujourdhui
        aujourdhui = date.today()
        auj = aujourdhui.strftime("%d/%m/%Y")
        #Il y a 7 jours
        jours = aujourdhui - timedelta(days=7)
        _7jours = jours.strftime("%Y-%m-%d")
        #Mois en cours
        jours = date.today()
        #Au debut du mois
        jours = jours.replace(day=1)
        _mois = jours.strftime("%Y-%m-%d")
        #Mois dernier
        jours = jours  - timedelta(days=1)
        _fin_mois_dernier = jours.strftime("%Y-%m-%d")
        jours = jours.replace(day=1)
        _debut_mois_dernier = jours.strftime("%Y-%m-%d")

        page = self.entete()
        page = page + '''<div><div class="titre">
                            <h3>Les chiffres du Coronavirus en temps réel <br>''' + auj + '''</h3>
                        </div>'''
        page = page + '<div class="box">'
        page = page + '''   <div class="conteneur_recap">
                                <div class="case_recap">
                                    <fieldset>
                                    <legend>
                                        Aujourd'hui
                                    </legend>
                                    <div>
                                        <div class="recap_nouveaux">''' + str(dao_patient.dao_Patient().get_nbr_nouveaux_patients_aujourdhui()) + ''' : Nouveaux</div>
                                        <div class="recap_gerrie">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_jour_etat(0)) + ''' : Guéris</div>
                                        <div class="recap_moyen">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_jour_etat(1)) + ''' : Etat moyen</div>
                                        <div class="recap_grave">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_jour_etat(2)) + ''' : Etat grave</div>
                                       <div class="recap_tres_grave"> ''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_jour_etat(3)) + ''' : Etat très grave</div>
                                        <div class="recap_decede">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_jour_etat(4)) + ''' : Décès</div>
                                    </div>
                                    </fieldset>
                                </div>
                                <div class="case_recap">
                                    <fieldset>
                                    <legend>
                                        Les 7 derniers jours
                                    </legend>
                                    <div>
                                        <div class="recap_nouveaux">''' + str(dao_patient.dao_Patient().get_nbr_patients_depuis(_7jours)) + ''' : Nouveaux patients</div>
                                        <div class="recap_gerrie">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(0, _7jours)) + ''' : Guéris</div>
                                        <div class="recap_moyen">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(1, _7jours)) + ''' : Etat moyen</div>
                                        <div class="recap_grave">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(2, _7jours)) + ''' : Etat grave</div>
                                        <div class="recap_tres_grave"> ''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(3, _7jours)) + ''' : Etat très grave</div>
                                        <div class="recap_decede">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(4, _7jours)) + ''' : Décès</div>
                                    </div>
                                    </fieldset>
                                </div>
                            </div>
                            <div class="conteneur_recap">
                                <div class="case_recap">
                                    <fieldset>
                                    <legend>
                                        Le mois en cours
                                    </legend>
                                    <div>
                                        <div class="recap_nouveaux">''' + str(dao_patient.dao_Patient().get_nbr_patients_depuis(_mois)) + ''' : Nouveaux patients</div>
                                        <div class="recap_gerrie">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(0, _mois)) + ''' : Guéris</div>
                                        <div class="recap_moyen">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(1, _mois)) + ''' : Etat moyen</div>
                                        <div class="recap_grave">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(2, _mois)) + ''' : Etat grave</div>
                                        <div class="recap_tres_grave"> ''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(3, _mois)) + ''' : Etat très grave</div>
                                        <div class="recap_decede">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_depuis(4, _mois)) + ''' : Décès</div>
                                    </div>
                                    </fieldset>
                                </div>
                                <div class="case_recap">
                                    <fieldset>
                                    <legend>
                                        Le mois dernier
                                    </legend>
                                    <div>
                                        <div class="recap_nouveaux">''' + str(dao_patient.dao_Patient().get_nbr_patients_dates(_debut_mois_dernier, _fin_mois_dernier)) + ''' : Nouveaux patients</div>
                                        <div class="recap_gerrie">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_dates(0, _debut_mois_dernier, _fin_mois_dernier)) + ''' : Guéris</div>
                                        <div class="recap_moyen">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_dates(1, _debut_mois_dernier, _fin_mois_dernier)) + ''' : Etat moyen</div>
                                        <div class="recap_grave">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_dates(2, _debut_mois_dernier, _fin_mois_dernier)) + ''' : Etat grave</div>
                                        <div class="recap_tres_grave">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_dates(3, _debut_mois_dernier, _fin_mois_dernier)) + ''' : Etat très grave</div>
                                        <div class="recap_decede">''' + str(dao_questionnaire.dao_Questionnaire().questionnaire_etat_dates(4, _debut_mois_dernier, _fin_mois_dernier)) + ''' : Décès</div>
                                    </div>
                                    </fieldset>
                                </div>
                            </div>'''
        page = page + '''</div>
        <div class="navigation_pages"><a href="/accueil/">Accueil</a></div>
        </div>'''
        page = page + self.footer()
        return page
    tableau_chiffres.exposed = True

    def get_acces_utilisateur(self, id_personne):
        pers = dao_personne.dao_Personne().get_personne(id_personne)
        dateN = pers.get_date_de_naiss()
        dateI = int(dateN.replace("-", "")) + pers.get_id()
        passe = hex(dateI)
        passe = passe.replace("0x", "")

        acc = acces.Acces()
        login = pers.get_prenom().lower()[0] + pers.get_nom().lower()[0] + "." + pers.get_nom().replace(" ", "").lower()
        acc.set_id_personne(id_personne)
        acc.set_login(login)
        #Mise en commentaire du cryptage pour l'exercice
        #passe = passe.encode()
        #passe = hashlib.sha1(passe).hexdigest()

        acc.set_mot_de_passe(passe)
        dao_acces.dao_Acces().insert_acces(acc)
        page = "Login : <b>" + login + "</b><br>Mot de passe : <b>" + passe + "</b>"
        return page


    def deconnexion(self) :
        model_global.deconnect_user()
        return self.vers_accueil()
    deconnexion.exposed = True

    def vers_accueil(self):
        return '<head><meta http-equiv="refresh" content="0;URL=/accueil/"></head>'
    deconnexion.exposed = True