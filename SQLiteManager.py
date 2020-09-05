#!/bin/env python
# coding=utf-8
import sqlite3


class SQLiteManager(object):

    def __init__(self) :
        self.fichier = "base.sq3"
        self.connexion = sqlite3.connect(self.fichier)
        self.cursor = self.connexion.cursor()

    def connect(self) :
        return self.cursor

    def commit(self) :
        self.connexion.commit()

    def cursor_close(self) :
        self.connexion.commit()

    def connexion_close(self) :
        self.connexion.commit()

    def close(self) :
        self.cursor.close()
        self.connexion.commit()
        self.connexion.close()

    def init_data_base(self):
        base = SQLiteManager()
        connect = base.connect()
        #Création des tables dans la base de données
        connect.execute('CREATE TABLE personnes (id INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(100), prenom VARCHAR(100), date_de_naissance DATE)')
        connect.execute('CREATE TABLE acces (id INTEGER PRIMARY KEY NOT NULL, login VARCHAR(100), mot_de_passe VARCHAR(100), id_personne INTEGER NOT NULL)')
        connect.execute('CREATE TABLE coordonnees (id INTEGER PRIMARY KEY NOT NULL, telephone VARCHAR(100), adresse_postale VARCHAR(100), adresse_mail VARCHAR(100), id_personne INTEGER NOT NULL)')
        connect.execute('CREATE TABLE medecins (id INTEGER PRIMARY KEY NOT NULL, rpps BIGINT NOT NULL liberal BOOLEAN, hopital VARCHAR(100), id_personne INTEGER NOT NULL)')
        connect.execute('CREATE TABLE patients (id INTEGER PRIMARY KEY NOT NULL, nss BIGINT NOT NULL, id_personne INTEGER NOT NULL, id_medecin INTEGER NOT NULL,)')
        connect.execute('CREATE TABLE questionnaires (id INTEGER PRIMARY KEY NOT NULL, date_q DATE, heure TIME, id_patient INTEGER NOT NULL)')
        connect.execute('''CREATE TABLE questions (id INTEGER PRIMARY KEY NOT NULL, intitule VARCHAR(200), description_q VARCHAR(1000), 
        valeur VARCHAR(100), niveau INTEGER NOT NULL, type_reponse VARCHAR(20) NOT NULL, reponse_alerte VARCHAR(20))''')
        connect.execute('CREATE TABLE reponses (id INTEGER PRIMARY KEY NOT NULL, reponse VARCHAR(1000), id_question INTEGER NOT NULL, id_questionnaire INTEGER NOT NULL)')
        connect.execute('ALTER TABLE questions ADD valeur VARCHAR(100)')
        connect.close()

    def test_agrs(self,*argv) :
        for ar in argv:
            print("Ils sont là :"+str(ar))

#SQLiteManager().test_agrs(1,2,3,4,5,6,7)

#SQLiteManager().init_data_base()

#from time import gmtime, strftime
#print(strftime("%Y%m%d_%H%M", gmtime()))




