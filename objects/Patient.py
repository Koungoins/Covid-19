#!/bin/env python
# coding=utf-8
from objects import personne

class Patient(personne.Personne):

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.nss = ""
        self.id_personne = -1

    #Saisir une personne avec tout ses attributs d'un seul coup
    def set_patient(self, id_patient, id_personne, nom, prenom, daten, nss):
        super().set_personne(id_patient, nom, prenom, daten)
        self.nss = nss
        self.id_personne = id_personne

    #Affichage
    def to_string(self) :
        return super().to_string() +", "+ str(self.nss) +", "+ str(self.id_personne)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement

    def set_nss(self, nss) :
        self.nss = nss

    def set_id_personne(self, id_personne) :
        self.id_personne = id_personne

    #Les GETTER permettent de récupérer les valeurs des attributs proprement

    def get_nss(self) :
        return self.nss

    def get_id_personne(self) :
        return self.id_personne