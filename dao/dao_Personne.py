import SQLiteManager as db
from objects import Personne as per

class dao_Personne :

    #Constructeur
    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM personnes")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        return max + 1


    #Récupère les données d'une personne dans la table personnes à l'aide de son ID et renvoi un objet Personne
    def get_personne(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, nom, prenom, date_de_naissance FROM personnes WHERE id = ?", id)
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Personne()
            p.set_personne(result[0][0], result[0][1], result[0][2], result[0][3])
        base.close()
        return p

    #Renvoi la liste de toutes les personnes
    def get_all(self) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, nom, prenom, date_de_naissance FROM personnes")
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Personne()
            pcur.set_personne(cur[0], cur[1], cur[2], cur[3])
            p.append(pcur)
        base.close()
        return p

    #Crée une nouvelle personne dans la table personne à l'aide des infos contenues dans l'objet Personne en argument
    def insert_personne(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("INSERT INTO personnes VALUES (?,?,?,?)",(self.next_id(), pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss()))
        base.close()

    #Crée une nouvelle personne dans la table personne à l'aide des infos en argument
    def insert_personne2(self, nom, prenom, date) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("INSERT INTO personnes VALUES (?, ?, ?, ?)",(self.next_id(), nom, prenom, date))
        base.close()

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_personne(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE personnes SET nom = ?, prenom = ? ,date_de_naissance = ? WHERE id = ?",
        (pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss(), pers.get_id()))
        base.close()

    #Met à jour les information d'une personne dans la table personne à l'aide des infos en argument
    def update_personne2(self, id, nom, prenom, date) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE personnes SET nom = ?, prenom = ? ,date_de_naissance = ? WHERE id = ?", (nom, prenom, date, id))
        base.close()

    #Supprime une personne dans la table personne
    def delete_personne(self, pers):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM personnes WHERE id = ?)",pers.get_id())
        base.close()

    #Supprime une personne dans la table personne
    def delete_personne2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM personne WHERE id = ?)", id)
        base.close()


