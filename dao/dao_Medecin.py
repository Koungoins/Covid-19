#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from dao import dao_personne
from objects import medecin
from objects import personne

class dao_Medecin(dao_personne.dao_Personne) :

    def __init__(self):
        print("")


    #Recherche si les acces existe
    def connexion(self, login, passe):
        base = db.SQLiteManager()
        cursor = base.connect()
        sql = '''SELECT med.id, med.id_personne, med.liberal, med.hopital, med.rpps
            FROM medecins AS med
            JOIN personnes AS pers ON med.id_personne = pers.id
            JOIN acces AS acc ON acc.id_personne = pers.id '''
        sql = sql + "WHERE acc.login LIKE '" + login + "' AND acc.mot_de_passe LIKE '" + passe + "' "
        cursor.execute(sql)
        result = cursor.fetchall()
        base.close()
        if len(result) > 0 :
            ac = medecin.Medecin()
            ac.set_medecin2(result[0][0], result[0][1], result[0][2], result[0][3], result[0][3])
            return ac
        else:
            return None

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


    def get_all_medecins(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT med.id, med.id_personne, med.liberal, med.hopital, med.rpps
                        FROM medecins AS med
                        JOIN personnes AS pers ON med.id_personne = pers.id''')
        result = cursor.fetchall()
        base.close()
        p = []
        med = None
        pcur = None
        for cur in result :
            pcur = super().get_personne(cur[1])
            med = medecin.Medecin()
            med.set_medecin(cur[0], cur[1], pcur.get_nom(), pcur.get_prenom(), pcur.get_date_de_naiss(), cur[2], cur[3], cur[4])
            p.append(med)
        return p

    #Crée un nouveau médecin dans la table personnes puis médecins à l'aide des infos contenues dans l'objet Medecin en argument
    def insert_medecin(self, medec) :
        id_personne = dao_personne.dao_Personne().insert_personne2(medec.get_nom(), medec.get_prenom(), medec.get_date_de_naiss())
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_medecin()
        cursor.execute("INSERT INTO medecins VALUES (?, ?, ?, ?, ?)",(current_id, medec.get_liberal(), medec.get_hopital(), id_personne, medec.get_rpps()))
        base.close()
        return current_id

    def get_medecin(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, id_personne, liberal, hopital, rpps FROM medecins WHERE id = "+str(id))
        result = cursor.fetchall()
        base.close()
        p = None
        if len(result) > 0 :
            p = medecin.Medecin()
            p.set_id(result[0][0])
            p.set_id_personne(result[0][1])
            p.set_liberal(result[0][2])
            p.set_hopital(result[0][3])
            p.set_rpps(result[0][4])
            #Infos personne
            pers = super().get_personne(p.get_id_personne())
            p.set_nom(pers.get_nom())
            p.set_prenom(pers.get_prenom())
            p.set_date_de_naiss(pers.get_date_de_naiss())
        return p


