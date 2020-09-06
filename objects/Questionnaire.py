#!/bin/env python
# coding=utf-8

class Questionnaire:

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.date = None
        self.heure = None
        self.id_patient = -1
        self.commentaire = ""

    #Saisir un acces avec tout ses attributs d'un seul coup
    def set_questionnaire(self, id, date, heure, id_patient, commentaire):
        self.id = id
        self.date = date
        self.heure = heure
        self.id_patient = id_patient
        self.commentaire = commentaire

    #Affichage
    def to_string(self) :
        return str(self.id) + ", " + self.date + "_" + self.heure + ", " + str(self.id_patient)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_date(self, date) :
        self.date = date

    def set_heure(self, heure) :
        self.heure = heure

    def set_id_patient(self, id_patient) :
        self.id_patient = id_patient

    def set_commentaire(self, commentaire) :
        self.commentaire = commentaire

    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_date(self) :
        return self.date

    def get_heure(self) :
        return self.heure

    def get_id_patient(self) :
        return self.id_patient

    def get_commentaire(self) :
        return self.commentaire