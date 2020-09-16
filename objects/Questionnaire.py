#!/bin/env python
# coding=utf-8

class Questionnaire(object) :

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.date = None
        self.heure = None
        self.id_patient = -1
        self.commentaire = ""
        self.analyse = ""
        self.reponses = []
        self.etat_patient = -1

    #Saisir un acces avec tout ses attributs d'un seul coup
    def set_questionnaire(self, id, date, heure, id_patient, commentaire, analyse):
        self.id = id
        self.date = date
        self.heure = heure
        self.id_patient = id_patient
        self.commentaire = commentaire
        self.analyse = analyse
        self.reponses = []
        self.etat_patient = -1

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

    def set_analyse(self, analyse) :
        self.analyse = analyse

    def set_reponses(self, reponses) :
        self.reponses = reponses

    def set_etat_patient(self, etat_patient) :
        self.etat_patient = etat_patient

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

    def get_analyse(self) :
        if self.analyse == None :
            return ""
        else :
            return self.analyse

    def get_reponses(self) :
        return self.reponses

    def get_etat_patient(self) :
        return self.etat_patient