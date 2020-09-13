#!/bin/env python
# coding=utf-8
from objects import personne

class Patient(personne.Personne):

    #Constructeur de la classe Personne
    def __init__(self):
        super().__init__()
        self.id = -1
        self.nss = ""
        self.id_personne = -1
        self.id_medecin = -1
        self.date_teste = None

    #Saisir une personne avec tout ses attributs d'un seul coup
    def set_patient(self, id_patient, id_personne, nom, prenom, daten, nss, id_medecin):
        super().set_personne(id_patient, nom, prenom, daten)
        self.set_patient2(id_patient, nss, id_personne, id_medecin)

    def set_patient2(self, id, nss, id_personne, id_medecin):
        self.id = id
        self.nss = nss
        self.id_personne = id_personne
        self.id_medecin = id_medecin
        self.date_teste = None

    #Affichage
    def to_string(self) :
        return super().get_nom() + " " + super().get_prenom() + " - "+ str(self.nss)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_nss(self, nss) :
        self.nss = nss

    def set_id_personne(self, id_personne) :
        self.id_personne = id_personne

    def set_id_medecin(self, id_medecin) :
        self.id_medecin = id_medecin

    def set_date_teste(self, date_teste) :
        self.date_teste = date_teste

    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_nss(self) :
        return self.nss

    def get_id_personne(self) :
        return self.id_personne

    def get_id_medecin(self) :
        return self.id_medecin

    def get_date_teste(self) :
        return self.date_teste