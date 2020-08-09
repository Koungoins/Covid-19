class Personne:

    #Constructeur de la classe Personne
    def __init__(self):
        self.id = -1
        self.nom = ""
        self.prenom = ""
        self.date_de_naiss = -1

    #Saisir une personne avec tout ses attributs d'un seul coup
    def set_personne(self, id, nom, prenom, date_de_naiss):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_de_naiss = date_de_naiss

    #Affichage
    def to_string(self) :
        return self.id , self.nom , self.prenom , self.date_de_naiss

    #Les SETTER permettent de saisirs les valeurs des attributs proprement
    def set_id(self, id) :
        self.id = id

    def set_nom(self, nom) :
        self.nom = nom

    def set_prenom(self, prenom) :
        self.prenom = prenom

    def set_date_de_naiss(self, date_de_naiss) :
        self.date_de_naiss = date_de_naiss


    #Les GETTER permettent de récupérer les valeurs des attributs proprement
    def get_id(self) :
        return self.id

    def get_nom(self) :
        return self.nom

    def get_prenom(self) :
        return self.prenom

    def get_date_de_naiss(self) :
        return  self.date_de_naiss
