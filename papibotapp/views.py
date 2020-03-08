import pdb

from flask import Flask, jsonify, render_template, request

from papibotapp.forms import EntryForm

from .grandpy import GrandPy

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object("papibotapp.config")
# To get one variable, tape app.config['MY_VARIABLE']


@app.route("/")
@app.route("/index/")
def home():
    return render_template(
        "pages/index.html", form=EntryForm(), gmapskey=app.config["GOOGLE_API_KEY"]
    )


@app.route("/response", methods=["POST"])
def response():
    granpy = GrandPy(request.form["text"])
    return granpy.bot_response


@app.route("/about")
def about():
    return render_template("pages/about.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
