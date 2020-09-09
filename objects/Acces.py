#!/bin/env python
# coding=utf-8

class Acces(object) :

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.login = None
        self.mot_de_passe = None
        self.id_personne = None

    #Saisir un acces avec tout ses attributs d'un seul coup
    def set_acces(self, id, login, mot_de_passe, id_personne):
        self.id = id
        self.login = login
        self.mot_de_passe = mot_de_passe
        self.id_personne = id_personne

    #Affichage
    def to_string(self) :
        return self.id , self.login , self.mot_de_passe , self.id_personne

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_login(self, login) :
        self.login = login

    def set_mot_de_passe(self, mot_de_passe) :
        self.mot_de_passe = mot_de_passe

    def set_id_personne(self, id_personne) :
        self.id_personne = id_personne


    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_login(self) :
        return self.login

    def get_mot_de_passe(self) :
        return self.mot_de_passe

    def get_id_personne(self) :
        return  self.id_personne
