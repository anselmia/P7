import pdb

from flask import Flask, jsonify, render_template, request

from .grandpy import GMAPS_API_KEY, BotResponse

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object("config")
# To get one variable, tape app.config['MY_VARIABLE']


@app.route("/")
@app.route("/index/")
def home():
    return render_template("pages/index.html", gmapskey=app.config["GMAPS_API_KEY"])


@app.route("/_response", methods=["POST"])
def response():
    print(request.form["user_message"])
    bot_response = BotResponse(request.form["user_message"])

    print(bot_response.user_message)
    wiki_reply = bot_response.wiki_response_html
    gmap_reply = bot_response.gmaps_response
    print(bot_response.user_message_parsed)
    gmaps_address = bot_response.address
    gmaps_name = bot_response.name
    gmaps_json = bot_response.gmaps_json

    return jsonify(
        wiki_reply=wiki_reply,
        gmaps_reply=gmap_reply,
        gmaps_address=gmaps_address,
        gmaps_name=gmaps_name,
        gmaps_json=gmaps_json,
    )


@app.route("/about")
def about():
    return render_template("pages/about.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
