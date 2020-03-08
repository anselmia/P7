import requests

from papibotapp.config import GOOGLE_API_KEY


class Map:
    """Contains all the google api"""

    def __init__(self, search):
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
            "fields": "formatted_address,geometry,name,place_id",
        }
        self.formatted_address = None
        self.get_response()

    def get_response(self):
        """return the response from arg"""

        request = requests.get(self.api_url, params=self.parameters).json()
        if request["status"] == "OK":
            self.formatted_address = request["candidates"][0]["formatted_address"]
            self.geometry = request["candidates"][0]["geometry"]
