"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, render_template
# from flask_restx import Resource, Api
# import db.db as db

app = Flask(__name__)
# api = Api(app)


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    """
    The `get()` method will return a list of available endpoints.
    """
    return render_template("home.html")
   
@app.route("/")
@app.route("/userPage", methods=['GET', 'POST'])
def userPage():
    return render_template("userPage.html")

@app.route("/")
@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")
    
@app.route("/")
@app.route("/searchPage", methods=['GET', 'POST'])
def searchPage():
    return render_template("searchPage.html")

@app.route("/")
@app.route("/recoveryPage", methods=['GET', 'POST'])
def recoveryPage():
    return render_template("recoveryPage.html")

if __name__ == '__main__':
    app.run()
