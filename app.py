import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
# from flask_login import login_user, logout_user, login_required
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def landing_page():
    return render_template("landing.html")


# Allow a user to register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)
    return render_template("register.html")


@app.route("/add_finisher", methods=["GET", "POST"])
def add_finisher():
    categories = mongo.db.categories.find()
    exercises = mongo.db.exercises.find()
    return render_template(
        "add_finisher.html", categories=categories, exercises=exercises)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
