#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import coordonnees as coor

class dao_Coordonnees(object)  :

    #Constructeur
    def __init__(self):
        print("")

    def next_id(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM coordonnees")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1

    #Récupère les données des coordonnées dans la table coordonnées à l'aide de son ID et renvoi un objet Coordonnées
    def get_coordonnees(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, telephone, adresse_postale, adresse_mail, id_personne FROM coordonnees WHERE id = ?", id)
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = coor.Coordonnees()
            p.set_coordonnees(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        base.close()
        return p

    #Renvoi les coordonnées d'une personne à l'aide de son id
    def get_coordonnees_personne(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, telephone, adresse_postale, adresse_mail, id_personne FROM coordonnees WHERE id_personne = ?", (id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = coor.Coordonnees()
            p.set_coordonnees(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        base.close()
        return p

    #Crée des nouvelles coordonnées dans la table coordonnées à l'aide des infos contenues dans l'objet Coordonnées en argument
    def insert_coordonnees(self, coord) :
        base = db.SQLiteManager()
        cursor = base.connect()
        id_next = self.next_id()
        cursor.execute("INSERT INTO coordonnees(id, telephone, adresse_postale, adresse_mail, id_personne) VALUES (?, ?, ?, ?, ?)",
        (id_next, coord.get_telephone(), coord.get_adresse_postale(), coord.get_adresse_mail(), coord.get_id_personne()))
        base.close()
        return id_next

    #Crée des nouvelles coordonnées dans la table acces à l'aide des infos en argument
    def insert_coordonnees2(self, telephone, adresse_postale, adresse_mail, id_personne) :
        base = db.SQLiteManager()
        cursor = base.connect()
        id_next = self.next_id()
        cursor.execute("INSERT INTO coordonnees VALUES (?, ?, ?, ?, ?)", (id_next, telephone, adresse_postale, adresse_mail, id_personne))
        base.close()
        return id_next

    #Met à jour les information des coordonnées dans la table coordonnées à l'aide des infos dans l'objet Coordonnées en argument
    def update_coordonnees(self, coord) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE coordonnees SET telephone = ?, adresse_postale = ?, adresse_mail = ? WHERE id = ?",
        (coord.get_telephone(), coord.get_adresse_postale(), coord.get_adresse_mail(), coord.get_id()))
        base.close()

    #Met à jour les information d'un acces dans la table acces à l'aide des infos en argument
    def update_coordonnees2(self, id, telephone, adresse_postale, adresse_mail, id_personne) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE coordonnees SET telephone = ?, adresse_postale = ?, adresse_mail = ? WHERE id = ?", (telephone, adresse_postale, adresse_mail, id))
        base.close()

    #Supprime une personne dans la table personne
    def delete_coordonnees(self, coordonnees):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM coordonnees WHERE id = ?)",coordonnees.get_id())
        base.close()

    #Supprime une personne dans la table personne
    def delete_coordonnees2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM coordonnees WHERE id = ?)", id)
        base.close()