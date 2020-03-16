""" Route description of the application """

from flask import Flask, render_template, request

from papibotapp.forms import EntryForm

from .grandpy import GrandPy

app = Flask(__name__)

# To get one variable, tape app.config['MY_VARIABLE']
app.config.from_object("papibotapp.config")


@app.route("/")
@app.route("/index/")
def home():
    """ Render Home page of the application """
    return render_template(
        "pages/index.html", form=EntryForm(), gmapskey=app.config["GOOGLE_API_KEY"]
    )


@app.route("/response", methods=["POST"])
def response():
    """ Bot response for place search request
        return :
        grandpy.bot_response
            - grandpy's answer
            - geometry from gmap and formated_address
            - extract from wikipedia
    """

    granpy = GrandPy(request.form["text"])
    return granpy.bot_response


@app.route("/about")
def about():
    """ Render About page of the application """
    return render_template("pages/about.html")


@app.errorhandler(404)
def page_not_found():
    """ Render error 404 page of the application """
    return render_template("errors/404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
