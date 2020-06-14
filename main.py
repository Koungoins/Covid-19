#!/bin/env python
# coding=utf-8
import threading as thread
from tkinter import *
from tkinter import ttk




class MainFrame  :

    #Declaration des variables de l'interface
    def __init__(self) :
        #Déclaration de la fenetre
        self.fenetre = Tk()
        self.fenetre['bg'] = 'grey'
        self.fenetre.configure(width = 800, height = 800)
        self.fenetre.title("titre_fenetre")

        #Affichage de la fenetre
        self.fenetre.mainloop()


#lance la fenetre dans le Thread principal
if __name__ == "__main__":
    print("Dans le Thread principal")
    f = thread.Thread(target = MainFrame)
    f.start()