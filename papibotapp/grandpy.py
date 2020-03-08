#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""

import random
import re
import urllib

import requests
from flask import jsonify

from papibotapp.answer import Answer
from papibotapp.config import GOOGLE_API_KEY
from papibotapp.map import Map
from papibotapp.parser import Parser
from papibotapp.wiki import Wiki


class GrandPy:
    """Contains main algorithms for the application"""

    def __init__(self, question):
        self.answer = Answer()
        self.grandpy_answer = None
        self.wiki_answer = None
        self.map_answer = None
        self.question = question
        self.cleaned_question = None
        self.wiki = None
        self.map = None

        self.bot_response = self.get_response()

    def json_answer(self):
        """Check answer and return them in the json format"""
        if self.map_answer is not None and self.wiki_answer is not None:
            return jsonify(
                {
                    "answer": self.grandpy_answer,
                    "wiki_answer": self.wiki_answer,
                    "map_answer": self.map_answer,
                }
            )
        elif self.map is not None:
            return jsonify({"answer": self.grandpy_answer, "map_answer": self.map_answer})
        elif self.wiki is not None:
            return jsonify({"answer": self.grandpy_answer, "wiki_answer": self.wiki_answer})
        else:
            return jsonify({"answer": self.grandpy_answer})

    def generate_questions(self):
        """Generate questions for parser and searches"""
        p = Parser(self.question)
        self.cleaned_question = p.clean_question()

    def get_response(self):
        """main function of answer"""
        self.generate_questions()
        self.check_easy_answer()
        if self.grandpy_answer is None:
            self.wiki = Wiki(self.cleaned_question)
            if self.wiki.answer is not None:
                self.wiki_answer = self.wiki.answer
            self.map = Map(self.cleaned_question)
            if self.map.geometry is not None:
                self.map_answer = {
                    "geometry": self.map.geometry,
                    "adress": self.map.formatted_address,
                }
            if self.map_answer is not None and self.wiki_answer is not None:
                self.grandpy_answer = self.answer.random_answer(self.answer.answer_location_find)
            else:
                self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        return self.json_answer()

    def check_easy_answer(self):
        random_answer = random
        """check if the answer deserve a simple answer"""
        if self.question.isdigit():
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        elif not re.search(r"[^.]", self.question):
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        elif not re.search(r"[^!]", self.question):
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        elif not re.search(r"[^zZ]", self.question):
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        elif not re.search("[a-zA-Z]", self.question):
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
        elif self.cleaned_question == "":
            self.grandpy_answer = self.answer.random_answer(self.answer.answer_stupid)
