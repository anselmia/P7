#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import requests

import papibotapp.map as mapapi
import papibotapp.wiki as wikiapi
from papibotapp.answer import Answer
from papibotapp.parser import Parser
from io import BytesIO


def test_parser():
    parser = Parser("Bonjour, 514sqddzaioué& où se trouve México&&& ???")
    assert parser.clean_question() == "bonjour 514sqddzaioué méxico "


def test_answer():
    answer = Answer()
    assert answer.random_answer(answer.answer_location_find) != ""
    assert answer.random_answer(answer.answer_stupid) != ""


################################################
##################### GMAP #####################
################################################


def test_geometry():
    gmap = mapapi.Map("Openclassrooms")
    assert gmap.geometry == {
        "location": {"lat": 48.8748465, "lng": 2.3504873},
        "viewport": {
            "northeast": {"lat": 48.87622362989272, "lng": 2.351843679892722},
            "southwest": {"lat": 48.87352397010727, "lng": 2.349144020107278},
        },
    }


def test_wikianswer():
    wiki = wikiapi.Wiki("Openclassrooms")
    assert (
        wiki.answer
        == 'OpenClassrooms est un site web de formation en ligne qui propose à ses membres des cours certifiants et des parcours débouchant sur des métiers en croissance. Ses contenus sont réalisés en interne, par des écoles, des universités, des entreprises partenaires comme Microsoft ou IBM, ou historiquement par des bénévoles. Jusqu\'en 2018, n\'importe quel membre du site pouvait être auteur, via un outil nommé « interface de rédaction » puis « Course Lab ». De nombreux cours sont issus de la communauté, mais ne sont plus mis en avant. Initialement orientée autour de la programmation informatique, la plate-forme couvre depuis 2013 des thématiques plus larges tels que le marketing, l\'entrepreneuriat et les sciences. <a href="http://fr.wikipedia.org/?curid=4338589" target="_blank">En savoir plus sur wikipédia.</a>'
    )

class MockResponse:
    '''Mock for requests.get response call'''
    def __init__(self, result, ok=True):
        self.ok = ok
        self.result = result

    def json(self):
        return self.result

def test_request_gmap(monkeypatch):
    result = [{
        "candidates":[
            {
                "formatted_address":"7 Cité Paradis, 75010 Paris, France",
                "geometry":{
                    "location":{
                        "lat":48.8748465,
                        "lng":2.3504873
                    },
                    "viewport":{
                        "northeast":{
                            "lat":48.87622362989272,
                            "lng":2.351843679892722
                        },
                        "southwest":{
                            "lat":48.87352397010727,
                            "lng":2.349144020107278
                        }
                    }
                },
                "name":"OpenClassrooms",
                "place_id":"ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"
            }
        ],
        "status":"OK"
    }]

    def mock_return(url, params):
        return MockResponse({
            "candidates":
                [{
                    "formatted_address":"7 Cité Paradis, 75010 Paris, France",
                    "geometry":{
                        "location":{
                            "lat":48.8748465,
                            "lng":2.3504873
                        },
                        "viewport":{
                            "northeast":{
                                "lat":48.87622362989272,
                                "lng":2.351843679892722
                            },
                            "southwest":{
                                "lat":48.87352397010727,
                                "lng":2.349144020107278
                            }
                        }
                    },
                    "name":"OpenClassrooms",
                    "place_id":"ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"
            }],
            "status":"OK"
        })

    monkeypatch.setattr(requests, "get", mock_return)
    gmap = mapapi.Map("Openclassrooms")
    gmap.get_response()
    assert gmap.geometry == result[0]["candidates"][0]["geometry"]

def test_request_wiki(monkeypatch):
    result = {
        "batchcomplete": "",
        "continue": {
            "gsroffset": 1,
            "continue": "gsroffset||"
        },
        "query": {
            "pageids": [
            "4338589"
            ],
            "pages": {
                "4338589": {
                    "pageid": 4338589,
                    "ns": 0,
                    "title": "OpenClassrooms",
                    "index": 1,
                    "extract": "OpenClassrooms est un site web de formation en ligne qui propose à ses membres des cours certifiants et des parcours débouchant sur des métiers en croissance. Ses contenus sont réalisés en interne, par des écoles, des universités, des entreprises partenaires comme Microsoft ou IBM, ou historiquement par des bénévoles. Jusqu'en 2018, n'importe quel membre du site pouvait être auteur, via un outil nommé « interface de rédaction » puis « Course Lab ». De nombreux cours sont issus de la communauté, mais ne sont plus mis en avant. Initialement orientée autour de la programmation informatique, la plate-forme couvre depuis 2013 des thématiques plus larges tels que le marketing, l'entrepreneuriat et les sciences."
                }
            }
        }
    }

    def mock_return(url, params):
        return MockResponse({
            "batchcomplete": "",
            "continue": {
                "gsroffset": 1,
                "continue": "gsroffset||"
            },
            "query": {
                "pageids": [
                "4338589"
                ],
                "pages": {
                    "4338589": {
                        "pageid": 4338589,
                        "ns": 0,
                        "title": "OpenClassrooms",
                        "index": 1,
                        "extract": "OpenClassrooms est un site web de formation en ligne qui propose à ses membres des cours certifiants et des parcours débouchant sur des métiers en croissance. Ses contenus sont réalisés en interne, par des écoles, des universités, des entreprises partenaires comme Microsoft ou IBM, ou historiquement par des bénévoles. Jusqu'en 2018, n'importe quel membre du site pouvait être auteur, via un outil nommé « interface de rédaction » puis « Course Lab ». De nombreux cours sont issus de la communauté, mais ne sont plus mis en avant. Initialement orientée autour de la programmation informatique, la plate-forme couvre depuis 2013 des thématiques plus larges tels que le marketing, l'entrepreneuriat et les sciences."
                    }
                }
            }
        })

    monkeypatch.setattr(requests, "get", mock_return)
    wiki = wikiapi.Wiki("Openclassrooms")
    wiki.get_response()
    assert wiki.wiki_json == result
