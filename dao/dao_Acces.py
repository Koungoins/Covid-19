#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import acces as acc

class dao_Acces(object) :

    #Constructeur
    def __init__(self):
        print("")


    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM acces")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1

    #Récupère les données d'un acces dans la table acces à l'aide de son ID et renvoi un objet Acces
    def get_acces(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, login, mot_de_passe, id_personne FROM acces WHERE id = ?", (id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = acc.Acces()
            p.set_acces(result[0][0], result[0][1], result[0][2], result[0][3])
        base.close()
        return p

    #Renvoi la liste de tous les acces
    def get_acces_personne(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, login, mot_de_passe, id_personne FROM acces WHERE id_personne = ?", (id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = acc.Acces()
            p.set_acces(result[0][0], result[0][1], result[0][2], result[0][3])
        base.close()
        return p

    #Crée un nouvel acces dans la table acces à l'aide des infos contenues dans l'objet Acces en argument
    def insert_acces(self, acces) :
        base = db.SQLiteManager()
        cursor = base.connect()
        id = self.next_id()
        cursor.execute("INSERT INTO acces VALUES (?, ?, ?, ?)", (id, acces.get_login(), acces.get_mot_de_passe(), acces.get_id_personne()))
        base.close()
        return id

    #Crée un nouvel acces dans la table acces à l'aide des infos en argument
    def insert_acces2(self, login, mot_de_passe, id_personne) :
        base = db.SQLiteManager()
        cursor = base.connect()
        id = self.next_id()
        cursor.execute("INSERT INTO acces VALUES (?, ?, ?, ?)",(id, login, mot_de_passe, id_personne))
        base.close()
        return id

    #Met à jour les information d'un acces dans la table acces à l'aide des infos dans l'objet Acces en argument
    def update_acces(self, acces) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE acces SET login = ?, mot_de_passe = ? WHERE id = ?",
        (acces.get_login(), acces.get_mot_de_passe(),  acces.get_id()))
        base.close()

    #Met à jour les information d'un acces dans la table acces à l'aide des infos en argument
    def update_acces2(self, id, login, mot_de_passe) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE acces SET login = ?, mot_de_passe = ? WHERE id = ?", (login, mot_de_passe, id))
        base.close()

    #Supprime une personne dans la table personne
    def delete_acces(self, acces):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM acces WHERE id = ?)",acces.get_id())
        base.close()

    #Supprime une personne dans la table personne
    def delete_acces2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM acces WHERE id = ?)", id)
        base.close()