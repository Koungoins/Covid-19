#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import questionnaire as per
from dao import dao_question

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

    def get_questionnaire(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, date_q, heure, id_patient, commentaire FROM questionnaires WHERE id = " + str(id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Questionnaire()
            p.set_questionnaire(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
        base.close()
        return p

    def get_last_questionnaire(self, id_patient) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT id, date_q, heure, id_patient, commentaire
                        FROM questionnaires
                        WHERE  id_patient = '''+ str(id_patient)+''' 
                        AND id=(SELECT MAX(id) FROM questionnaires WHERE id_patient = '''+ str(id_patient)+''')''')
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Questionnaire()
            p.set_questionnaire(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
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
        cursor.execute("UPDATE questions SET intitule = ?, description_q = ?, valeur = ?, niveau = ? WHERE id = ?",
        (pers.get_intitule(), pers.get_description(), pers.get_valeur(), pers.get_niveau(), pers.get_id()))
        base.close()


    def update_questionnaire2(self, id, intitule, description, niveau) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE questions SET intitule = ?, description_q = ?, valeur = ?, niveau = ? WHERE id = ?", (intitule, description, niveau, id))
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