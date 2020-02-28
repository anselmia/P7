#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module used for GrandPy Bot
Stopword list used from https://github.com/stopwords-iso/stopwords-fr/blob/master/stopwords-fr.json
"""
import json
import os
import re
import urllib
import requests
from config import GMAPS_API_KEY


class BotResponse:
    def __init__(self, user_message):
        # Adding space before and after message for parsing.
        self.user_message = user_message
        self.user_message_parsed = self.parse_text()
        self.name = "No result"
        self.address = "No result"
        self.wiki_response_html = (
            "Je n'ai pas compris la demande ou je ne connais pas d'histoire à ce sujet."
        )
        self.wiki_json = ""
        self.gmaps_response = "No result"
        self.gmaps_json = ""

        if self.user_message_parsed != "":
            self.wiki_response_html = self.get_wiki_info()
            self.gmaps_response = self.get_gmaps_info()

    def parse_text(self):
        """Parses the attribute self.user_message. Sets chars to lowerkey, strips punctuation and removes words
        that are in stopwords.json. Returns user_message_parsed
        :rtype: string
        """
        try:
            with open(os.path.dirname(os.path.abspath(__file__)) + "\\stopword.json") as f:
                stopwords = json.load(f)
        except IOError as err:
            print("Error loading stopword file : " + str(err))
            stopwords = "error"

        # Remove all punctuation and make text lowercase with a regex

        string_no_punctuation = re.sub(r"[-,.;@#?!&$'()<>/]+ *", " ", self.user_message.lower(),)

        words_to_parse = string_no_punctuation.split()
        result_words = []

        for word in words_to_parse:
            if word not in stopwords:
                result_words.append(word)
        parsed_text = " ".join(result_words)

        return parsed_text

    def get_wiki_info(self):
        """Gets the 5 first sentences from wikipedia for the article about the parsed text
        :rtype: string
        """
        search_term = self.user_message_parsed
        api_url = "https://fr.wikipedia.org/w/api.php"
        payload = {
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "format": "json",
            "indexpageids": 1,
            "exsentences": 5,
            "generator": "search",
            "gsrlimit": 1,
            "gsrsearch": search_term,
        }

        resp = requests.get(api_url, params=payload)
        self.wiki_json = json.loads(resp.text)

        try:
            article_id = self.wiki_json["query"]["pageids"][0]
            wiki_article_intro = self.wiki_json["query"]["pages"][article_id]["extract"]
            wiki_link = "http://fr.wikipedia.org/?curid=" + article_id
            wiki_article_intro = (
                wiki_article_intro
                + ' <a href="'
                + wiki_link
                + '" target="_blank">En savoir plus sur wikipédia.</a>'
            )

        except KeyError:
            wiki_article_intro = self.wiki_response_html

        return wiki_article_intro

    def build_URL(self, search_text='',types_text=''):
        base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'     # Can change json to xml to change output type
        key_string = '?key='+ GMAPS_API_KEY                                           # First think after the base_url starts with ? instead of &
        query_string = '&query='+urllib.parse.quote(search_text)
        sensor_string = '&sensor=false'                                             # Presumably you are not getting location from device GPS
        type_string = ''                   # More on types: https://developers.google.com/places/documentation/supported_types
        url = base_url+key_string+query_string+sensor_string+type_string
        return url

    def get_gmaps_info(self):
        """Gets the information from gmaps about the parsed text, returns googlemaps_response and
        sets gmaps_json, name, and address if ok.
        :rtype: string
        """

        api_url = self.build_URL(self.user_message_parsed)

        resp = requests.get(api_url)
        data = json.loads(resp.text)

        self.gmaps_json = data
        print(data['status'])
        if data['status'] != 'ZERO_RESULTS':
            try:
                self.name = data['candidates'][0]['name']
                self.address = data['candidates'][0]['formatted_address']
            except IndexError:
                return "No result"
            return "OK"
        else:
            return "No result"
