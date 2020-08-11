#!/bin/env python
# coding=utf-8
from objects import personne

class Medecin(personne.Personne):

    #Constructeur de la classe Médecin
    def __init__(self):
        super().__init__()
        self.id_personne = -1
        self.liberal = False
        self.hopital = ""

    #Saisir un médecin avec tout ses attributs d'un seul coup
    def set_medecin(self, id_medecin, id_personne, nom, prenom, date_de_naiss, liberal, hopital):
        super().set_personne(id_medecin, nom, prenom, date_de_naiss)
        self.id_personne = id_personne
        self.liberal = liberal
        self.hopital = hopital

    #Affichage
    def to_string(self) :
        return super().to_string() + str(self.liberal) + ", " + self.hopital

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_liberal(self, liberal) :
        self.liberal = liberal

    def set_hopital(self, nom) :
        self.hopital = nom

    def set_id_personne(self, id_personne) :
        self.id_personne = id_personne


    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_liberal(self) :
        return self.liberal

    def get_hopital(self) :
        return self.hopital

    def get_id_personne(self) :
        return self.id_personne
