#!/bin/env python
# coding=utf-8

class Reponse(object):

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.reponse = None
        self.id_question = None
        self.id_questionnaire = None

    #Saisir un acces avec tout ses attributs d'un seul coup
    def set_reponse2(self, id, reponse, id_question, id_questionnaire):
        self.id = id
        self.reponse = reponse
        self.id_question = id_question
        self.id_questionnaire = id_questionnaire

    #Affichage
    def to_string(self) :
        return str(self.id) + ", " + self.reponse +", " + str(self.id_question) + ", " + str(self.id_questionnaire)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_reponse(self, reponse) :
        self.reponse = reponse

    def set_id_question(self, id_question) :
        self.id_question = id_question

    def set_id_questionnaire(self, id_questionnaire) :
        self.id_questionnaire = id_questionnaire

    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_reponse(self) :
        return self.reponse

    def get_id_question(self) :
        return self.id_question

    def get_id_questionnaire(self) :
        return self.id_questionnaire