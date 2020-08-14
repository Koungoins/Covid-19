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
        #connect.execute('CREATE TABLE personnes (id INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(100), prenom VARCHAR(100), date_de_naissance DATE)')
        #connect.execute('CREATE TABLE acces (id INTEGER PRIMARY KEY NOT NULL, login VARCHAR(100), mot_de_passe VARCHAR(100), id_personne INTEGER NOT NULL)')
        #connect.execute('CREATE TABLE coordonnees (id INTEGER PRIMARY KEY NOT NULL, telephone VARCHAR(100), adresse_postale VARCHAR(100), adresse_mail VARCHAR(100), id_personne INTEGER NOT NULL)')
        #connect.execute('CREATE TABLE medecins (id INTEGER PRIMARY KEY NOT NULL, rpps BIGINT NOT NULL liberal BOOLEAN, hopital VARCHAR(100), id_personne INTEGER NOT NULL)')
        #connect.execute('CREATE TABLE patients (id INTEGER PRIMARY KEY NOT NULL, nss BIGINT NOT NULL, id_personne INTEGER NOT NULL, id_medecin INTEGER NOT NULL,)')
        #connect.execute('ALTER TABLE medecins ADD rpps BIGINT')
        connect.close()

