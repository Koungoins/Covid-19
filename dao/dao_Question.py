#!/bin/env python
# coding=utf-8
import SQLiteManager as db
from objects import question as per

class dao_Question(object)  :

    #Constructeur
    def __init__(self):
        print("")

    #Renvoi l'identifiant suivant en incrémentant l'id max dans la table
    def next_id_question(self):
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT MAX(id) FROM questions")
        result = cursor.fetchall()
        max = 1
        if len(result) > 0 :
            max = result[0][0]
        base.close()
        if max == None : max = 0
        return max + 1


    def get_question(self, id) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, intitule, description_q, valeur, niveau, type_reponse, reponse_alerte FROM questions WHERE id = " + str(id))
        result = cursor.fetchall()
        p = None
        if len(result) > 0 :
            p = per.Question()
            p.set_question(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6])
        base.close()
        return p


    def get_all_questions(self) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, intitule, description_q, valeur, niveau, type_reponse, reponse_alerte FROM questions")
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Question()
            pcur.set_question(cur[0], cur[1], cur[2], cur[3], cur[4], cur[5], cur[6])
            p.append(pcur)
        base.close()
        return p

    def get_questions_niveau(self, niveau) :
        base = db.SQLiteManager()
        cursor = base.connect()
        cursor.execute("SELECT id, intitule, description_q, valeur, niveau, type_reponse, reponse_alerte FROM questions WHERE niveau = " + str(niveau))
        result = cursor.fetchall()
        p = []
        pcur = None
        for cur in result :
            pcur = per.Question()
            pcur.set_question(cur[0], cur[1], cur[2], cur[3], cur[4], cur[5], cur[6])
            p.append(pcur)
        base.close()
        return p

    #Crée une nouvelle personne dans la table personne à l'aide des infos contenues dans l'objet Personne en argument
    def insert_question(self, pers) :
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_question()
        cursor.execute("INSERT INTO questions (id, intitule, description_q, valeur, niveau, type_reponse, reponse_alerte) VALUES (?, ?, ?, ?, ?, ?)",
        (current_id, pers.get_intitule(), pers.get_description(), pers.valeur(), pers.niveau(), pers.type_reponse(), pers.reponse_alerte()))
        base.close()
        return current_id

    #Crée une nouvelle personne dans la table personne à l'aide des infos en argument
    def insert_question2(self, intitule, description, valeur, niveau, type_reponse, reponse_alerte) :
        base = db.SQLiteManager()
        cursor = base.connect()
        current_id = self.next_id_question()
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