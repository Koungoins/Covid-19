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
        sql = '''SELECT med.id, med.id_personne, pers.nom, pers.prenom, pers.date_de_naissance, med.liberal, med.hopital, med.rpps
            FROM medecins AS med
            JOIN personnes AS pers ON med.id_personne = pers.id
            JOIN acces AS acc ON acc.id_personne = pers.id '''
        sql = sql + "WHERE acc.login LIKE '" + login + "' AND acc.mot_de_passe LIKE '" + passe + "' "
        cursor.execute(sql)
        result = cursor.fetchall()
        base.close()
        if len(result) > 0 :
            ac = medecin.Medecin()
            ac.set_medecin(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7])
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
        cursor.execute('''SELECT med.id, med.id_personne, pers.nom, pers.prenom, pers.date_de_naissance, med.liberal, med.hopital, med.rpps
                        FROM medecins AS med
                        JOIN personnes AS pers ON med.id_personne = pers.id''')
        result = cursor.fetchall()
        base.close()
        p = []
        med = None
        for cur in result :
            med = medecin.Medecin()
            med.set_medecin(cur[0], cur[1], cur[2], cur[3], cur[4], cur[5], cur[6], cur[7])
            p.append(med)
        return p

    #Crée un nouveau médecin dans la table personnes puis médecins à l'aide des infos contenues dans l'objet Medecin en argument
    def insert_medecin(self, medec) :
        id_personne = dao_personne.dao_Personne().insert_personne2(medec.get_nom(), medec.get_prenom(), medec.get_date_de_naiss())
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_medecin()
        cursor.execute("INSERT INTO medecins (id, liberal, hopital, id_personne, rpps) VALUES (?, ?, ?, ?, ?)",(current_id, medec.get_liberal(), medec.get_hopital(), id_personne, medec.get_rpps()))
        base.close()
        return current_id

    def get_medecin(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT med.id, med.id_personne, med.liberal, med.hopital, med.rpps, pers.nom, pers.prenom, pers.date_de_naissance
                            FROM medecins AS med
                            JOIN personnes AS pers ON med.id_personne = pers.id
                            WHERE med.id =  ''' + str(id))
        result = cursor.fetchall()
        base.close()
        p = None
        if len(result) > 0 :
            p = medecin.Medecin()
            p.set_medecin(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7])
        return p


