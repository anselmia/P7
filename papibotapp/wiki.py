""" Module Import """

import json
import re

import requests


class Wiki:
    """ Class to request the wiki api
        Init with attribute search type : string
    """

    def __init__(self, search):
        """ Init function of the class Wiki """

        self.api_url = "https://fr.wikipedia.org/w/api.php"
        self.search = search
        self.parameters = {
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "format": "json",
            "indexpageids": 1,
            "exsentences": 5,
            "generator": "search",
            "gsrlimit": 1,
            "gsrsearch": self.search,
        }
        self.answer = None
        self.get_response()

    def get_response(self):
        """ Get article data from a search text"""
        """ Return an abstract of the article and link to read more
        :rtype: string
        """
        api_url = "https://fr.wikipedia.org/w/api.php"

        resp = requests.get(api_url, params=self.parameters).json()
        self.wiki_json = resp

        try:
            article_id = self.wiki_json["query"]["pageids"][0]
            wiki_article_intro = self.wiki_json["query"]["pages"][article_id]["extract"]
            wiki_link = "http://fr.wikipedia.org/?curid=" + article_id
            self.answer = (
                wiki_article_intro
                + ' <a href="'
                + wiki_link
                + '" target="_blank">En savoir plus sur wikipédia.</a>'
            )

        except KeyError:
            return

def Test_wiki():
    wiki = Wiki("OpenClassrooms")
    assert wiki.api_url == "https://fr.wikipedia.org/w/api.php"
    assert wiki.search == "OpenClassrooms"
    assert len(wiki.parameters) > 0
    assert wiki.answer != None

if __name__ == "__main__":
    Test_wiki()