"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, render_template
# from flask_restx import Resource, Api
# import db.db as db

app = Flask(__name__)
# api = Api(app)

loggedIn = False

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    """
    The `get()` method will return a list of available endpoints.
    """
    print("in here")
    if loggedIn == True:
        return render_template("home.html")
    return render_template("homeAnon.html")
   
@app.route("/userPage", methods=['GET', 'POST'])
def userPage():
    tempUserName = 'User01'
    # return render_template("home.html",user=tempUserName)
    print("going to user page")
    return render_template("userPage.html", user=tempUserName)

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()
