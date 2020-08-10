from dao import dao_Personne
from objects import Personne
import cherrypy

class html_Personne:



    def __init__(self):
        self.id_edite = -1

    #Page ajouter une personne
    @cherrypy.expose
    def index(self):
        page = self.liste()
        return page

    #Formulaire pour ajouter une personne
    @cherrypy.expose
    def ajouter(self):
        page = '''
        <title>Créer un nouveau patient</title>
        <h1>Créer un nouveau patient</h1>
        <form action="enregistrer" method="GET">
            <div>
                <label for="nom">Nom:</label>
                <input type="text" id="nom" name="nom_patient"><br>
                <label for="prenom">Prénom:</label>
                <input type="text" id="prenom" name="prenom_patient"><br>
                <label for="dateN">Date de naissance:</label>
                <input type="date" id="dateN" name="date_patient"><br>
                <input type="submit" value="Enregistrer">
            </div>
        </form>
        '''
        return page


    #Affiche la liste des personnes dans la base
    @cherrypy.expose
    def liste(self):
        page = "Les des personnes : <a href='ajouter'> Ajouter</a>"
        liste = dao_Personne.dao_Personne().get_all()
        for c in liste :
            #page = page + "<br><a href='edit?id="+str(c.get_id())+">"+c.to_string()+"</a>"
            page = page + '<br>' + c.to_string() + '<a href="edit?id=' + str(c.get_id())+'">Editer</a>, <a href="supprimer?id=' + str(c.get_id()) + '">Supprimer</a>'
        return page

    #Enregistre les information saisie dans le formulaire et affiche la liste des personnes enregistrées
    @cherrypy.expose
    def enregistrer(self, nom_patient = "", prenom_patient = "", date_patient = -1):
        p = Personne.Personne()
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        #Enregistrement et récupère l'id
        id = dao_Personne.dao_Personne().insert_personne(p)
        #Recherche la personne dans la base
        pliste = dao_Personne.dao_Personne().get_personne(id)
        page ="Nouvelle personne : <br>"
        page = page + pliste.to_string()
        page = page + '''
        <form action="liste"><input type="submit" value="Liste des personnes"></form>
        '''
        return page

    #Formulaire permettant de modifier les infos d'une personne
    @cherrypy.expose
    def edit(self, id):
        self.id_edite = id
        page = "<h1>Edition d'une personne</h1>"
        p = dao_Personne.dao_Personne().get_personne(id)
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

    #Met à jour les infos d'edition dans la base
    @cherrypy.expose
    def update(self, nom_patient, prenom_patient, date_patient):
        p = Personne.Personne()
        p.set_id(self.id_edite)
        p.set_nom(nom_patient)
        p.set_prenom(prenom_patient)
        p.set_date_de_naiss(date_patient)
        #Enregistrement et récupère l'id
        dao_Personne.dao_Personne().update_personne(p)
        #Recherche la personne dans la base
        pliste = dao_Personne.dao_Personne().get_personne(self.id_edite)
        page = pliste.to_string()
        return page

    #Supprime la personne dans la base
    @cherrypy.expose
    def supprimer(self, id):
        dao_Personne.dao_Personne().delete_personne2(id)
        page = "Personne supprimée.<br>"
        page = page + self.liste()
        return page
