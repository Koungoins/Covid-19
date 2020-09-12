#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from dao import dao_personne
from dao import dao_coordonnees
from objects import personne
from objects import patient
from objects import coordonnees



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

    #Nombre de nouveaux patients aujourd'hui
    def get_nbr_nouveaux_patients_aujourdhui(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT COUNT(*)
                            FROM patients 
                            WHERE date_teste = CURRENT_DATE''')
        result = cursor.fetchall()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max

    #Nombre de nouveaux patients depuis 
    def get_nbr_patients_depuis(self, debut):
        base = db.SQLiteManager()
        cursor = base.connect()
        requete = "SELECT COUNT(*) FROM patients  WHERE date_teste BETWEEN \'" + str(debut) + "\' AND  CURRENT_DATE"
        cursor.execute(requete)
        result = cursor.fetchall()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max


#Nombre de nouveaux patients aujourd'hui
    def get_nbr_patients_dates(self, debut, fin):
        base = db.SQLiteManager()
        cursor = base.connect()
        requete = "SELECT COUNT(*) FROM patients  WHERE date_teste BETWEEN \'" + str(debut) + "\' AND  \'" + str(fin) + "\'"
        cursor.execute(requete)
        result = cursor.fetchall()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max

    #Récupère les données d'un patient dans la table patients à l'aide de son ID et renvoi un objet Patient
    def get_patient(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, nss, id_personne, id_medecin, date_teste FROM patients WHERE id = " + str(id))
        result = cursor.fetchall()
        base.close()
        p = None
        if len(result) > 0 :
            p = patient.Patient()
            p.set_id(result[0][0])
            p.set_nss(result[0][1])
            p.set_id_personne(result[0][2])
            p.set_id_medecin(result[0][3])
            p.set_date_teste(result[0][4])
        pers = super().get_personne(p.get_id_personne())
        p.set_nom(pers.get_nom())
        p.set_prenom(pers.get_prenom())
        p.set_date_de_naiss(pers.get_date_de_naiss())
        coord = dao_coordonnees.dao_Coordonnees().get_coordonnees_personne(p.get_id_personne())
        p.set_coordonnees2(coord)
        return p

    #Renvoi la liste de toutes les personnes
    def get_patients_medecin(self, id_medecin, recherche) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT pat.id, pat.id_personne, pers.nom, pers.prenom, pers.date_de_naissance, pat.nss, pat.id_medecin
                        FROM patients AS pat
                        JOIN personnes AS pers ON pers.id = pat.id_personne
                        WHERE pat.id_medecin = ''' + str(id_medecin) + ''' AND 
                        (pers.nom LIKE '%''' + recherche + '''%' OR pers.prenom LIKE '%''' + recherche + '''%' OR pat.nss LIKE '%''' + recherche + '''%') ''')
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            #id_patient, id_personne, nom, prenom, daten, nss, id_medecin
            pcur = patient.Patient()
            pcur.set_patient(cur[0], cur[1], cur[2], cur[3], cur[4], cur[5], cur[6])
            p.append(pcur)
        base.close()
        return p

    #Crée une nouvelle personne dans la table personne à l'aide des infos contenues dans l'objet Personne en argument
    def insert_patient(self, pat) :
        id_pers = super().insert_personne2(pat.get_nom(), pat.get_prenom(), pat.get_date_de_naiss())
        dao_coordonnees.dao_Coordonnees().insert_coordonnees(pat.get_coordonnees())
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_patient()
        cursor.execute("INSERT INTO patients (id, nss, id_personne, id_medecin, date_teste) VALUES (?, ?, ?, ?, ?)",
        (current_id, pat.get_nss(), id_pers, pat.get_id_medecin(), pat.get_date_teste()))
        base.close()
        return current_id

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_patient(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE patients SET nss = ?, prenom = ?, date_de_naissance = ?, nss = ? WHERE id = ?",
        (pers.get_nom(), pers.get_prenom(), pers.get_date_de_naiss(), pers.get_id()))
        base.close()