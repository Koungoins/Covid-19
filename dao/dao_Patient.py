#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from dao import dao_personne
from objects import personne
from objects import patient



class dao_Patient(dao_personne.dao_Personne) :

    #Constructeur
    def __init__(self):
        print("")


    #Recherche si les acces existe
    def connexion(self, login, passe):
        base = db.SQLiteManager()
        cursor = base.connect()
        sql  =  '''SELECT pat.id, pat.nss, pat.id_personne, pat.id_medecin
        FROM patients AS pat
        JOIN personnes AS pers ON pat.id_personne = pers.id
        JOIN acces AS acc ON acc.id_personne = pers.id '''
        sql = sql + "WHERE acc.login LIKE '"+login+"' AND acc.mot_de_passe LIKE '"+passe+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        base.close()
        if len(result) > 0 :
            ac = patient.Patient()
            ac.set_patient2(result[0][0], result[0][1], result[0][2], result[0][3])
            return ac
        else:
            return None

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_patient(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM patients")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1


    #Récupère les données d'un patient dans la table patients à l'aide de son ID et renvoi un objet Patient
    def get_patient(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, nss, id_personne FROM patients WHERE id = "+str(id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = patient.Patient()
            p.set_id(result[0][0])
            p.set_nss(result[0][1])
            p.set_id_personne(result[0][2])
        base.close()
        pers = super().get_personne(p.get_id_personne())
        p.set_nom(pers.get_nom())
        p.set_prenom(pers.get_prenom())
        p.set_date_de_naiss(pers.get_date_de_naiss())
        return p

    #Renvoi la liste de toutes les personnes
    def get_all_patients(self) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, nss, id_personne FROM patients")
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = patient.Patient()
            pcur.set_id(cur[0])
            pcur.set_nss(cur[1])
            pcur.set_id_personne(cur[2])
            #Recherche des infos personnes
            per = dao_personne.dao_Personne().get_personne(pcur.get_id_personne())
            pcur.set_personne(per.get_id(), per.get_nom(), per.get_prenom(), per.get_date_de_naiss())
            p.append(pcur)
        base.close()
        return p

    #Crée une nouvelle personne dans la table personne à l'aide des infos contenues dans l'objet Personne en argument
    def insert_patient(self, pat) :
        id_pers = super().insert_personne2(pat.get_nom(), pat.get_prenom(), pat.get_date_de_naiss())
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_patient()
        cursor.execute("INSERT INTO patients(id, nss, id_personne) VALUES (?,?,?)",(current_id, pat.get_nss(), id_pers))
        base.close()
        return current_id

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_patient(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE personnes SET nom = ?, prenom = ? ,date_de_naissance = ? WHERE id = ?",
        (pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss(), pers.get_id()))
        base.close()