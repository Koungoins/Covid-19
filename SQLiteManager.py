import sqlite3


class SQLiteManager :

    def __init__(self) :
        self.fichier = "base.sq3"
        self.connexion = sqlite3.connect(self.fichier)
        self.cursor = self.connexion.cursor()

    def connect(self) :
        return self.cursor

    def close(self) :
        self.connexion.commit()
        self.cursor.close()
        self.connexion.close()

    def init_data_base(self):
        base = SQLiteManager()
        connect = base.connect()
        connect.execute('CREATE TABLE personnes (id INTEGER PRIMARY KEY NOT NULL, nom VARCHAR(100), prenom VARCHAR(100), date_de_naissance DATE)')
        connect.close()

