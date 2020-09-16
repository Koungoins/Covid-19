#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import reponse as per

class dao_Reponse(object)  :

    #Constructeur
    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_reponse(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM reponses")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1


    def get_reponse(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, reponse, id_question, id_questionnaire FROM reponses WHERE id = " + str(id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Reponse()
            p.set_reponse2(result[0][0], result[0][1], result[0][2], result[0][3])
        base.close()
        return p

    def get_last_reponse_patient(self, id_patient, niveau) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT rep.reponse, rep.id_question 
                        FROM reponses AS rep
                        JOIN questions AS qu ON rep.id_question = qu.id
                        JOIN questionnaires AS quest ON rep.id_questionnaire = quest.id
                        WHERE  quest.id_patient = ''' + str(id_patient) + ''' AND qu.niveau = ''' + str(niveau) + ''' AND 
                        quest.id=(SELECT MAX(id) FROM questionnaires WHERE id_patient = ''' + str(id_patient) + ''')''')
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Reponse()
            pcur.set_reponse(cur[0])
            pcur.set_id_question(cur[1])
            p.append(pcur)
        base.close()
        return p


    def get_reponses_questionnaire2(self, id_questionnaire) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute('''SELECT rep.id, rep.reponse, rep.id_question, rep.id_questionnaire, qu.id
                        FROM reponses AS rep
                        JOIN questions AS qu ON rep.id_question = qu.id
                        JOIN questionnaires AS quest ON rep.id_questionnaire = quest.id
                        WHERE  quest.id = ''' + str(id_questionnaire) + ''' ORDER BY qu.id''')
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Reponse()
            pcur.set_id(cur[0])
            pcur.set_reponse(cur[1])
            pcur.set_id_question(cur[2])
            pcur.set_id_questionnaire(cur[3])
            p.append(pcur)
        base.close()
        return p

    def get_reponses_questionnaire(self, id_questionnaire, niveau) :
        base = db.SQLiteManager()
        cursor = base.connect()
        req = '''SELECT rep.id, rep.reponse, rep.id_question, rep.id_questionnaire, qu.id
                        FROM reponses AS rep
                        JOIN questions AS qu ON rep.id_question = qu.id
                        JOIN questionnaires AS quest ON rep.id_questionnaire = quest.id
                        WHERE  quest.id = ''' + str(id_questionnaire) + ''' AND qu.niveau = ''' + str(niveau) + ''' ORDER BY qu.id'''
        print(req)
        cursor.execute(req)
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Reponse()
            pcur.set_id(cur[0])
            pcur.set_reponse(cur[1])
            pcur.set_id_question(cur[2])
            pcur.set_id_question(cur[3])
            p.append(pcur)
        base.close()
        return p

    def get_all_reponses(self) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, reponse, id_question, id_questionnaire FROM reponses")
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Reponse()
            pcur.set_reponse2(cur[0], cur[1], cur[2], cur[3])
            p.append(pcur)
        base.close()
        return p

    #Crée une nouvelle personne dans la table personne à l'aide des infos contenues dans l'objet Personne en argument
    def insert_reponse(self, pers) :
        current_id = self.next_id_reponse()
        base = db.SQLiteManager()
        cursor = base.connect()
        
        cursor.execute("INSERT INTO reponses (id, reponse, id_question, id_questionnaire) VALUES (?, ?, ?, ?)",
        (current_id, pers.get_reponse(), pers.get_id_question(), pers.get_id_questionnaire()))
        base.close()
        return current_id

    #Crée une nouvelle personne dans la table personne à l'aide des infos en argument
    def insert_reponse2(self, intitule, description, valeur, niveau, type_reponse, reponse_alerte) :
        current_id = self.next_id_reponse()
        base = db.SQLiteManager()
        cursor = base.connect()
        
        cursor.execute("INSERT INTO questions (id, intitule, description_q, valeur, niveau, type_reponse, reponse_alerte) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (current_id, intitule, description, valeur, niveau, type_reponse, reponse_alerte))
        base.close()
        return current_id

    #Met à jour les information d'une personne dans la table personne à l'aide des infos dans l'objet Personne en argument
    def update_question(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE questions SET intitule = ?, description_q = ?, valeur = ?, niveau = ? , type_reponse = ?, reponse_alerte = ? WHERE id = ?",
        (pers.get_intitule(), pers.get_description(), pers.get_valeur(), pers.get_niveau(), pers.get_type_reponse(), pers.get_reponse_alerte(), pers.get_id()))
        base.close()


    def update_question2(self, id, intitule, description, niveau, type_reponse, reponse_alerte) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("UPDATE questions SET intitule = ?, description_q = ?, valeur = ?, niveau = ?, type_reponse = ?, reponse_alerte = ? WHERE id = ?", 
        (intitule, description, niveau, type_reponse, id))
        base.close()


    def delete_question(self, pers):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM questions WHERE id = ?", (pers.get_id()))
        base.close()


    def delete_question2(self, id):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("DELETE FROM questions WHERE id = "+ str(id))
        base.close()