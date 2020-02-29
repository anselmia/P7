#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""

import re
import urllib

import requests
from flask import jsonify
from unidecode import unidecode

from papibotapp.answer import Answer
from papibotapp.config import GOOGLE_API_KEY
from papibotapp.map import Map
from papibotapp.parser import Parser
from papibotapp.wiki import Wiki


class GrandPy:
    """Contains main algorithms for the application"""

    def __init__(self, question):
        self.answer = None
        self.wiki_answer = None
        self.map_answer = None
        self.question = question
        self.parsed_question = None
        self.cleaned_question = None
        self.wiki = None
        self.map = None

    def json_answer(self):
        """Check answer and return them in the json format"""
        if self.map_answer and self.wiki_answer:
            return jsonify(
                {
                    "answer": self.answer,
                    "wiki_answer": self.wiki_answer,
                    "geometry": self.map.geometry,
                }
            )
        elif self.map_answer:
            return jsonify({"answer": self.answer, "geometry": self.map.geometry,})
        elif self.wiki_answer:
            return jsonify({"answer": self.answer, "wiki_answer": self.wiki_answer})
        else:
            return jsonify({"answer": self.answer})

    def clean_question_from_false_spaces(self):
        """clean and return a string without separating special chars"""
        newquestion = self.question
        newquestion = newquestion.replace("'", " ")
        newquestion = newquestion.replace("-", " ")
        return newquestion

    def clean_question_from_list(self, lst):
        """clean the questions of indesirable characters"""
        list_question = self.question.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub("[^A-Za-z0-9]+", "", x.lower()))
        new_list_question = [x for x in new_list_question if x.lower() not in lst]
        return " ".join(new_list_question)

    def clean_question_for_search(self):
        """return the final searched words"""
        questioncleaned = self.parsed_question
        list_question = questioncleaned.split(" ")
        new_list_question = []
        for x in list_question:
            new_list_question.append(re.sub("[^A-Za-z0-9]+", "", x.lower()))
        return " ".join(new_list_question)

    def generate_questions(self):
        """Generate questions for parser and searches"""
        self.question = unidecode(self.question)
        self.question = self.clean_question_from_false_spaces()
        self.parsed_question = self.clean_question_from_list(p.stop_words)
        self.cleaned_question = self.clean_question_for_search()

    def grandpyTalk(self):
        """main function of answer"""
        self.generate_questions()
        self.check_easy_answer()
        if self.answer is None:
            self.wiki = Wiki(self.cleaned_question)
            if self.wiki.response:
                self.wiki_answer = self.wiki.response
            self.map = Map(self.cleaned_question)

            self.answer = a.random_answer(a.answer_location_find)
            self.map_answer = a.random_answer(a.answer_location_here)
        return self.json_answer()

    def check_easy_answer(self):
        """check if the answer deserve a simple answer"""
        if self.question.isdigit():
            self.answer = a.get_stupid_answer(0)
        elif "merci" in self.question.lower():
            self.answer = a.get_stupid_answer(5)
        elif "bonjour" in self.question.lower():
            self.answer = a.random_answer(a.answer_hello)
        elif not re.search(r"[^.]", self.question):
            self.answer = a.get_stupid_answer(1)
        elif not re.search(r"[^!]", self.question):
            self.answer = a.get_stupid_answer(2)
        elif not re.search(r"[^zZ]", self.question):
            self.answer = a.get_stupid_answer(3)
        elif not re.search("[a-zA-Z]", self.question):
            self.answer = a.get_stupid_answer(4)
        elif self.cleaned_question == "":
            self.answer = a.random_answer(Answer.answer_too_old)

    def grandpy_find_wiki(self):
        """Return an answer with the wiki api"""
        self.answer = a.random_answer(a.answer_wiki_find)
        if self.wiki.is_location():
            self.map_answer = a.random_answer(a.answer_location_here)
            self.coord_lat = self.wiki.lat
            self.coord_long = self.wiki.long
            self.wiki_answer = self.wiki.getSummary()
        else:
            self.wiki_answer = self.wiki.getSummary()


p = Parser()
a = Answer()
