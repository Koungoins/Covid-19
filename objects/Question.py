#!/bin/env python
# coding=utf-8

class Question:

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.intitule = None
        self.description = None
        self.niveau = None
        self.valeur = None
        self.type_reponse = None
        self.reponse_alerte = None
        self.comparateur = 2

    #Saisir un acces avec tout ses attributs d'un seul coup
    def set_question(self, id, intitule, description, valeur, niveau, type_reponse, reponse_alerte, comparateur):
        self.id = id
        self.intitule = intitule
        self.description = description
        self.niveau = niveau
        self.valeur = valeur
        self.type_reponse = type_reponse
        self.reponse_alerte = None
        self.comparateur = comparateur

    #Affichage
    def to_string(self) :
        return str(self.id) + ", <b>" + self.intitule + "</b><br>" + self.description + ", " + self.valeur + ", " + str(self.niveau) + ", " + self.type_reponse + ", " + str(self.reponse_alerte)

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_intitule(self, intitule) :
        self.intitule = intitule

    def set_description(self, description) :
        self.description = description

    def set_niveau(self, niveau) :
        self.niveau = niveau

    def set_valeur(self, valeur) :
        self.valeur = valeur

    def set_type_reponse(self, type_reponse) :
        self.type_reponse = type_reponse

    def set_reponse_alerte(self, reponse_alerte) :
        self.reponse_alerte = reponse_alerte

    def set_comparateur(self, comparateur) :
        self.comparateur = comparateur


    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_intitule(self) :
        return self.intitule

    def get_description(self) :
        return self.description

    def get_niveau(self) :
        return self.niveau

    def get_valeur(self) :
        return self.valeur

    def get_type_reponse(self) :
        return self.type_reponse

    def get_reponse_alerte(self) :
        return self.reponse_alerte

    def get_comparateur(self) :
        return self.comparateur