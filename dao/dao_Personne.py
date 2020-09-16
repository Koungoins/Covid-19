#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import personne as per
from objects import coordonnees
from dao import dao_coordonnees

class dao_Personne(object)  :

    #Constructeur
    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_personne(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM personnes")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1


    #Récupère les données d'une personne dans la table personnes à l'aide de son ID et renvoi un objet Personne
    def get_personne(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        req = "SELECT id, nom, prenom, date_de_naissance FROM personnes WHERE id = " + str(id)
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        base.close()
        p = None
        if len(result) > 0 :
            p = per.Personne()
            p.set_id(result[0][0])
            p.set_nom(result[0][1])
            p.set_prenom(result[0][2])
            p.set_date_de_naiss(result[0][3])
            coord = dao_coordonnees.dao_Coordonnees().get_coordonnees_personne(p.get_id())
            p.set_coordonnees2(coord)
        return p

    #Renvoi la liste de toutes les personnes
    def get_all_personnes(self) :
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
        current_id = self.next_id_personne()
        base = db.SQLiteManager()
        cursor = base.connect()
        
        cursor.execute("INSERT INTO personnes VALUES (?,?,?,?)",(current_id, pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss()))
        base.close()
        return current_id

    #Crée une nouvelle personne dans la table personne à l'aide des infos en argument
    def insert_personne2(self, nom, prenom, date) :
        current_id = self.next_id_personne()
        base = db.SQLiteManager()
        cursor = base.connect()
        
        cursor.execute("INSERT INTO personnes VALUES (?, ?, ?, ?)",(current_id, nom, prenom, date))
        base.close()
        return current_id

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_personne(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE personnes SET nom = ?, prenom = ?, date_de_naissance = ? WHERE id = ?",
        (pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss(), pers.get_id()))
        base.close()
        coord = pers.get_coordonnees()
        coord.set_id_personne(pers.get_id())
        dao_coordonnees.dao_Coordonnees().update_coordonnees(coord)

    #Met à jour les information d'une personne dans la table personne à l'aide des infos en argument
    def update_personne2(self, id, nom, prenom, date) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE personnes SET nom = ?, prenom = ?, date_de_naissance = ? WHERE id = ?", (nom, prenom, date, id))
        base.close()

    #Supprime une personne dans la table personne
    def delete_personne(self, pers):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM personnes WHERE id = ?", (pers.get_id()))
        base.close()

    #Supprime une personne dans la table personne
    def delete_personne2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM personnes WHERE id = "+ str(id))
        base.close()