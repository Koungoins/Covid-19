#!/bin/env python
# coding=utf-8
import cherrypy

from objects import question
from dao import dao_question

from html import html_globale
import model_global

class Pages_Questions(html_globale.Page_Globale) :

    def __init__(self):
        self.titre_page = "Espace Questions"

    def index(self):
        return self.liste_questions()
    index.exposed = True

    def liste_questions(self):
        return "Liste des questions ici"
    liste_questions.exposed = True