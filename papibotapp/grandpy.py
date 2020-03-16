"""
    Module import
"""

import re

from flask import Flask

from papibotapp.answer import Answer
from papibotapp.map import Map
from papibotapp.parse import Parser
from papibotapp.wiki import Wiki


class GrandPy:
    """
        Main class of the application
        Interact with class Map, Wiki, Parser and answer.
        Init with attribute question
    """

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
        response = {}
        response["answer"] = self.grandpy_answer
        if self.map_answer is not None:
            response["map_answer"] = self.map_answer
        if self.wiki_answer is not None:
            response["wiki_answer"] = self.wiki_answer
        return response

    def generate_questions(self):
        """Generate questions for parser and searches"""
        p = Parser(self.question)
        self.cleaned_question = p.clean_question()

    def get_response(self):
        """
            main function
            Interact with class Map, Wiki, Parser and answer
            to get an answer from each.
        """
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
        """ check if the answer deserve a simple answer """

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

def test_granpy():
    """ Module test """

    app = Flask(__name__)
    with app.app_context():
        grandpy = GrandPy("OpenClassrooms??./:!")
        bot_response = grandpy.get_response()
        assert "answer" in bot_response
        assert "wiki_answer" in bot_response
        assert "map_answer" in bot_response

        grandpy = GrandPy("")
        bot_response = grandpy.get_response()
        assert "answer" in bot_response
        assert "wiki_answer" not in bot_response
        assert "map_answer" not in bot_response

if __name__ == "__main__":
    test_granpy()
