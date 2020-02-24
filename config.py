import os

if os.environ.get("GMAPS_API_KEY") is None:
    with open(os.path.join(os.path.dirname(__file__), "api_key_local"), "r") as api_key_local:
        GMAPS_API_KEY = api_key_local.read()

else:
    GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")
