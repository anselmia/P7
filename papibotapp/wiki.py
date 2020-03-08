import json
import re

import requests


class Wiki:
    """Contains all the wiki api"""

    def __init__(self, search):
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
        """Get article data from a title"""
        """Gets the 5 first sentences from wikipedia for the article about the parsed text
        :rtype: string
        """
        api_url = "https://fr.wikipedia.org/w/api.php"

        resp = requests.get(api_url, params=self.parameters)
        self.wiki_json = json.loads(resp.text)

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
