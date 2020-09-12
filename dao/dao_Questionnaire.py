#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import questionnaire as per
from dao import dao_question
from dao import dao_reponse
from datetime import date


class dao_Questionnaire(object)  :

    #Constructeur
    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_questionnaire(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM questionnaires")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1

    def questionnaire_jour_etat(self, etat):
        base = db.SQLiteManager()
        cursor = base.connect()
        req = '''SELECT COUNT(DISTINCT id_patient)
                            FROM questionnaires
                            WHERE date_q = CURRENT_DATE AND etat_patient = ''' + str(etat)
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        base.close()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        return max

    def questionnaire_etat_dates(self, etat, debut, fin):
        base = db.SQLiteManager()
        cursor = base.connect()
        req = "SELECT COUNT(DISTINCT id_patient) FROM questionnaires WHERE etat_patient = " + str(etat) + " AND date_q BETWEEN \'" + str(debut) + "\' AND  \'" + str(fin) + "\'"
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        base.close()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        return max

    def questionnaire_etat_depuis(self, etat, date):
        base = db.SQLiteManager()
        cursor = base.connect()
        req = "SELECT COUNT(DISTINCT id_patient) FROM questionnaires WHERE etat_patient = " + str(etat) + " AND date_q BETWEEN \'" + str(date) + "\' AND  CURRENT_DATE "
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        base.close()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        return max

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def jour_rempli(self, id_patient):
        aujourdhui = date.today()
        auj = aujourdhui.strftime("%Y-%m-%d")
        base = db.SQLiteManager()
        cursor = base.connect()
        req = "SELECT COUNT(*) FROM questionnaires WHERE id_patient=2 AND date_q=\'" + auj + "\'"
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        max = 0
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max


    def get_questionnaire(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, date_q, heure, id_patient, commentaire, analyse FROM questionnaires WHERE id = " + str(id))
        result = cursor.fetchall()
        base.close()
        p = None
        if len(result) > 0 :
            p = per.Questionnaire()
            p.set_questionnaire(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
            p.set_reponses(dao_reponse.dao_Reponse().get_reponses_questionnaire2(id))
        return p

    #Donne les questionnaires du patient du plus recent au plus ancien
    def get_questionnaires_patient(self, id, niveau) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT id, date_q, heure, id_patient, commentaire, analyse
                            FROM questionnaires
                            WHERE id_patient = ''' + str(id) + '''
                            ORDER BY date_q DESC''')
        result = cursor.fetchall()
        base.close()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Questionnaire()
            pcur.set_id(cur[0])
            pcur.set_date(cur[1])
            pcur.set_heure(cur[2])
            pcur.set_id_patient(cur[3])
            pcur.set_commentaire(cur[4])
            pcur.set_analyse(cur[5])
            #Recupere les reponses
            pcur.set_reponses(dao_reponse.dao_Reponse().get_reponses_questionnaire(id, niveau))
            p.append(pcur)
        return p

    def get_last_questionnaire(self, id_patient) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT id, date_q, heure, id_patient, commentaire, analyse
                        FROM questionnaires
                        WHERE  id_patient = '''+ str(id_patient)+''' 
                        AND id=(SELECT MAX(id) FROM questionnaires WHERE id_patient = '''+ str(id_patient)+''')''')
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Questionnaire()
            p.set_questionnaire(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
        base.close()
        return p


    #Crée une nouveau questionnaire dans la table questionnaires à l'aide des infos contenues dans l'objet Questionnaire en argument
    def insert_questionnaire(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_questionnaire()
        cursor.execute("INSERT INTO questionnaires (id, date_q, heure, id_patient, commentaire) VALUES (?, ?, ?, ?, ?)",
        (current_id, pers.get_date(), pers.get_heure(), pers.get_id_patient(), pers.get_commentaire()))
        base.close()
        return current_id

    #Crée une nouvelle personne dans la table personne à l'aide des infos en argument
    def insert_questionnaire2(self, intitule, description, valeur, niveau, commentaire) :
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_questionnaire()
        cursor.execute("INSERT INTO questions (id, intitule, description_q, valeur, niveau, commentaire) VALUES (?, ?, ?, ?, ?, ?)",
        (current_id, intitule, description, valeur, niveau, commentaire))
        base.close()
        return current_id

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_questionnaire(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE questionnaires SET analyser = ? WHERE id = ?", (pers.get_analyser, pers.get_id()))
        base.close()


    def update_questionnaire2(self, id, analyse, etat_patient) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE questionnaires SET analyse = ?, etat_patient = ? WHERE id = ?", (analyse, etat_patient, id))
        base.close()


    def delete_questionnaire(self, pers):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM questions WHERE id = ?", (pers.get_id()))
        base.close()


    def delete_questionnaire2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM questions WHERE id = "+ str(id))
        base.close()