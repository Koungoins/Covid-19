#!/bin/env python
# coding=utf-8
from objects import coordonnees

class Personne:

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.nom = ""
        self.prenom = ""
        self.date_de_naiss = ""
        self.coordonnees = None

    #Saisir une personne avec tout ses attributs d'un seul coup
    def set_personne(self, id, nom, prenom, date_de_naiss):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_de_naiss = date_de_naiss

    #Affichage
    def to_string(self) :
        return str(self.id) +", "+ self.nom +", "+ self.prenom +", "+ str(self.date_de_naiss)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_nom(self, nom) :
        self.nom = nom

    def set_prenom(self, prenom) :
        self.prenom = prenom

    def set_date_de_naiss(self, date_de_naiss) :
        self.date_de_naiss = date_de_naiss

    def set_coordonnees(self, telephone, ad_postale, mail):
        coord = coordonnees.Coordonnees()
        coord.set_telephone(telephone)
        coord.set_adresse_postale(ad_postale)
        coord.set_adresse_mail(mail)
        coord.set_id_personne(self.get_id())
        self.coordonnees = coord

    def set_coordonnees2(self, coord):
        self.coordonnees = coord

    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_nom(self) :
        return self.nom

    def get_prenom(self) :
        return self.prenom

    def get_date_de_naiss(self) :
        return  self.date_de_naiss

    def get_coordonnees(self):
        return self.coordonnees
