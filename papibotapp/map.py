""" Module import """

import requests

from papibotapp.config import GOOGLE_API_KEY


class Map:
    """
        Class to communicate with google find place api
        Init with attribute search, place to find within the google aî
    """

    def __init__(self, search):
        """Init function of class Map"""

        self.api_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        self.search = search
        self.geometry = None
        self.parameters = {
            "key": GOOGLE_API_KEY,
            "inputtype": "textquery",
            "locationbias": "point:48.856614,2.3522219",
            "language": "fr",
            "input": self.search,
            "type": "street_address",
            "fields": "formatted_address,geometry",
        }
        self.formatted_address = None
        self.get_response()

    def get_response(self):
        """ request gmap api """

        request = requests.get(self.api_url, params=self.parameters).json()
        if request["status"] == "OK":
            self.formatted_address = request["candidates"][0]["formatted_address"]
            self.geometry = request["candidates"][0]["geometry"]

def test_map():
    map = Map("OpenClassrooms")
    assert map.api_url == "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    assert map.search == "OpenClassrooms"
    assert len(map.parameters) > 0
    assert map.geometry != None
    assert map.formatted_address != None

if __name__ == "__main__":
    test_map()