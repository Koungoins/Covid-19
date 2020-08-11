#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from dao import dao_personne

class dao_Medecin(dao_personne.dao_Personne) :

    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_medecin(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM medecins")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1

    #Crée un nouveau médecin dans la table personnes puis médecins à l'aide des infos contenues dans l'objet Medecin en argument
    def insert_medecin(self, medec) :
        id_personne = dao_personne.dao_Personne().insert_personne2(medec.get_nom(), medec.get_prenom(), medec.get_date_de_naiss())
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_medecin()
        cursor.execute("INSERT INTO medecins VALUES (?, ?, ?, ?)",(current_id, medec.get_liberal(), medec.get_hopital(), id_personne))
        base.close()
        return current_id


