#!/bin/env python
# coding=utf-8

class Coordonnees(object) :

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.telephone = ""
        self.adresse_postale = ""
        self.adresse_mail = ""
        self.id_personne = -1

    #Saisir des coordonnées avec tout ses attributs d'un seul coup
    def set_coordonnees(self, id, telephone, adresse_postale, adresse_mail, id_personne):
        self.id = id
        self.telephone = telephone
        self.adresse_postale = adresse_postale
        self.adresse_mail = adresse_mail
        self.id_personne = id_personne

    #Affichage
    def to_string(self) :
        return self.id , self.telephone , self.adresse_postale , self.adresse_mail, self.id_personne

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_telephone(self, telephone) :
        self.telephone = telephone

    def set_adresse_postale(self, adresse_postale) :
        self.adresse_postale = adresse_postale

    def set_adresse_mail(self, adresse_mail) :
        self.adresse_mail = adresse_mail

    def set_id_personne(self, id_personne) :
        self.id_personne = id_personne


    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_telephone(self) :
        return self.telephone

    def get_adresse_postale(self) :
        return self.adresse_postale

    def get_adresse_mail(self) :
        return self.adresse_mail

    def get_id_personne(self) :
        return  self.id_personne