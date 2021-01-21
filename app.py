import os
from flask import (
    Flask, flash, render_template,
    redirect, request, url_for, jsonify)
from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import (
    StringField, PasswordField, TextAreaField, RadioField)
from wtforms.validators import InputRequired, Length, Regexp, EqualTo
from flask_login import (
    UserMixin, LoginManager, current_user,
    login_user, logout_user, login_required)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
CsrfProtect(app)

mongo = PyMongo(app)


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json
        self.username = self.user_json.get("username")
        self.library = self.user_json.get("library")
        self.is_admin = self.user_json.get("is_admin")

    def get_id(self):
        object_id = self.user_json.get("_id")
        return str(object_id)


@login_manager.user_loader
def load_user(user_id):
    user_obj = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_obj)


class registration_form(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(
        min=5, max=20, message="Must be between 5 and 20 characters long"),
        Regexp("^[a-zA-Z0-9_]*$",
               message="Please use letters and/or numbers only")])
    password = PasswordField("password", validators=[InputRequired(), Length(
        min=5, max=20, message="Must be between 5 and 20 characters long"),
        Regexp("^[a-zA-Z0-9_]*$",
               message="Please use letters and/or numbers only")])
    confirm = PasswordField("Repeat Password", validators=[EqualTo(
        "password", message='Passwords must match')])


class login_form(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(
        min=5, max=20, message="Must be between 5 and 20 characters long"),
        Regexp("^[a-zA-Z0-9_]*$",
               message="Please use letters and/or numbers only")])
    password = PasswordField("password", validators=[InputRequired(), Length(
        min=5, max=20, message="Must be between 5 and 20 characters long"),
        Regexp("^[a-zA-Z0-9_]*$",
               message="Please use letters and/or numbers only")])


class review_form(FlaskForm):
    vote = RadioField("vote", choices=[(100, "upvote"), (0, "downvote")])
    review = TextAreaField("review", validators=[InputRequired()])


class add_exercise(FlaskForm):
    exercise_name = StringField(
        "Exercise name:", validators=[InputRequired(), Length(
            min=3, max=50,
            message="Must be between 5 and 50 characters long")])


@app.route("/")
def home_page():
    return render_template("home.html")


# Allow a user to register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = registration_form()
    if form.validate_on_submit():

        username_taken = mongo.db.users.find_one(
            {"username": form.username.data.lower()})

        if username_taken:
            flash("Username already taken")
            return redirect(url_for("register"))

        new_user = {
            "username": form.username.data.lower(),
            "password": generate_password_hash(form.password.data),
            "library": [],
            "is_admin": False
        }

        mongo.db.users.insert_one(new_user)
        username_exists = mongo.db.users.find_one(
            {"username": form.username.data.lower()})
        loginUser = User(username_exists)
        login_user(loginUser)

        return redirect(url_for("dashboard", username=new_user["username"]))

    return render_template("register.html", form=form)


# Allow a user to login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = login_form()

    if form.validate_on_submit():
        username_exists = mongo.db.users.find_one(
            {"username": form.username.data.lower()})

        if username_exists:

            if check_password_hash(
                    username_exists["password"],
                    form.password.data):
                loginUser = User(username_exists)
                login_user(loginUser)
                return redirect(url_for(
                    "dashboard", username=username_exists["username"]))

            else:
                flash("Invalid username and/or password")
                return redirect(url_for("login"))

        else:
            flash("Invalid username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


# Display the user's dashboard
@app.route("/dashboard/<username>", methods=["GET", "POST"])
@login_required
def dashboard(username):
    finishers = mongo.db.finishers.find({"created_by": current_user.username})
    added_finishers = mongo.db.finishers.find(
        {"_id": {"$in": current_user.library}})

    if current_user.is_authenticated:
        return render_template(
            "dashboard.html", username=current_user.username,
            finishers=finishers, added_finishers=added_finishers)

    return redirect(url_for("login"))


# Allow a user to add a finisher to the database
@app.route("/add_finisher", methods=["GET", "POST"])
@login_required
def add_finisher():
    categories = mongo.db.categories.find()

    if request.method == "POST":
        form_input_nested = [[], [], []]
        for key, val in request.form.items():
            if key.startswith("exercise"):
                form_input_nested[0].append(val)
            if key.startswith("reps"):
                form_input_nested[1].append(val)
            if key.startswith("set_type"):
                form_input_nested[2].append(val)

        # sort form_input_nested into an
        # array of objects using list comprehension
        exercises = [{"exercise_name": a,
                      "set": b,
                      "set_type": c
                      } for (a, b, c) in zip(*form_input_nested)]
        time_limit_toggle = "on" if request.form.get(
            "time_limit_toggle") else "off"
        finisher = {
            "finisher_name": request.form.get("finisher_name"),
            "category_name": request.form.get("categories"),
            "exercises": exercises,
            "time_limit_toggle": time_limit_toggle,
            "time_limit": request.form.get("time_limit"),
            "instructions": request.form.get("instructions"),
            "reviews": [],
            "votes": [],
            "created_by": current_user.username
        }

        mongo.db.finishers.insert_one(finisher)
        return redirect(url_for("dashboard", username=current_user.username))

    return render_template(
        "add_finisher.html", categories=categories)


# Allow a user to edit a finisher and then add to their library
# This creates a new finisher that is a modified version of an existing one
@app.route("/edit_finisher/<finisher_id>", methods=["GET", "POST"])
@login_required
def edit_finisher(finisher_id):
    finisher = mongo.db.finishers.find_one({"_id": ObjectId(finisher_id)})
    categories = mongo.db.categories.find()

    if request.method == "POST":
        form_input_nested = [[], [], []]
        for key, val in request.form.items():
            if key.startswith("exercise"):
                form_input_nested[0].append(val)
            if key.startswith("reps"):
                form_input_nested[1].append(val)
            if key.startswith("set_type"):
                form_input_nested[2].append(val)

        # sort form_input_nested into an array of objects
        exercises = [{"exercise_name": a,
                      "set": b,
                      "set_type": c
                      } for (a, b, c) in zip(*form_input_nested)]
        time_limit_toggle = "on" if request.form.get(
            "time_limit_toggle") else "off"
        edited_finisher = {
            "finisher_name": request.form.get("finisher_name"),
            "category_name": request.form.get("categories"),
            "exercises": exercises,
            "time_limit_toggle": time_limit_toggle,
            "time_limit": request.form.get("time_limit"),
            "instructions": request.form.get("instructions"),
            "reviews": [],
            "votes": [],
            "created_by": current_user.username
        }

        if request.form.get("finisher_name") == finisher["finisher_name"]:
            flash("Please give a new name to the edited finisher")
        else:
            mongo.db.finishers.insert_one(edited_finisher)
            return redirect(url_for(
                "dashboard", username=current_user.username))

    return render_template(
        "edit_finisher.html", finisher=finisher, categories=categories)


# Allow a user to edit a finisher they created
# This doesn't create a new finisher in the collection
@app.route("/modify_finisher/<finisher_id>", methods=["GET", "POST"])
@login_required
def modify_finisher(finisher_id):
    finisher = mongo.db.finishers.find_one({"_id": ObjectId(finisher_id)})
    categories = mongo.db.categories.find()

    if request.method == "POST":
        form_input_nested = [[], [], []]
        for key, val in request.form.items():
            if key.startswith("exercise"):
                form_input_nested[0].append(val)
            if key.startswith("reps"):
                form_input_nested[1].append(val)
            if key.startswith("set_type"):
                form_input_nested[2].append(val)
        # sort form_input_nested into an array of objects
        exercises = [{"exercise_name": a,
                      "set": b,
                      "set_type": c
                      } for (a, b, c) in zip(*form_input_nested)]
        time_limit_toggle = "on" if request.form.get(
            "time_limit_toggle") else "off"
        modified_finisher = {
            "finisher_name": request.form.get("finisher_name"),
            "category_name": request.form.get("categories"),
            "exercises": exercises,
            "time_limit_toggle": time_limit_toggle,
            "time_limit": request.form.get("time_limit"),
            "instructions": request.form.get("instructions"),
            "reviews": finisher["reviews"],
            "votes": finisher["votes"],
            "created_by": current_user.username
        }
        mongo.db.finishers.update(
            {"_id": ObjectId(finisher_id)}, modified_finisher)
        return redirect(url_for("dashboard", username=current_user.username))
    return render_template(
        "modify_finisher.html", finisher=finisher, categories=categories)


# User can add a finisher to their library without editing
@app.route("/add_to_library/<finisher_id>")
def add_to_library(finisher_id):
    finisher = mongo.db.finishers.find_one(
        {"_id": ObjectId(finisher_id)})["_id"]
    mongo.db.users.update(
        {"username": current_user.username}, {"$push": {"library": finisher}})

    flash("Finisher added to library")
    return redirect(url_for("dashboard", username=current_user.username))


# User can remove a finisher from their library without deleting it from DB
@app.route("/remove_from_library/<finisher_id>")
def remove_from_library(finisher_id):
    finisher = mongo.db.finishers.find_one(
        {"_id": ObjectId(finisher_id)})["_id"]

    mongo.db.users.update(
        {"username": current_user.username}, {"$pull": {"library": finisher}})

    flash("Finisher removed from library")
    return redirect(url_for("dashboard", username=current_user.username))


# Allows a user to completely delete a finisher they authored
@app.route("/delete_finisher/<finisher_id>")
@login_required
def delete_finisher(finisher_id):
    finisher_creator = mongo.db.finishers.find_one(
        {"_id": ObjectId(finisher_id)})["created_by"]

    if current_user.username == finisher_creator:
        mongo.db.finishers.remove({"_id": ObjectId(finisher_id)})
        flash("Finisher deleted")
        return redirect(url_for("dashboard", username=current_user.username))

    else:
        flash("You can only delete finishers you have created")
        return redirect(url_for("dashboard", username=current_user.username))


# Shows an individual finisher and allows a user to review it
@app.route("/finisher/<finisher_id>", methods=["GET", "POST"])
@login_required
def display_finisher(finisher_id):
    form = review_form()
    finisher = mongo.db.finishers.find_one(
        {"_id": ObjectId(finisher_id)})
    categories = list(mongo.db.categories.find())
    reviews = list(finisher["reviews"])
    ratings = [int(i) for i in finisher["votes"]]
    if len(ratings) != 0:
        rating = sum(ratings)/len(ratings)
    else:
        rating = 0

    if form.validate_on_submit():

        review = {
            "review": form.review.data,
            "reviewed_by": current_user.username
        }
        mongo.db.finishers.update(
            {"_id": ObjectId(finisher_id)}, {"$push": {"reviews": review}})
        mongo.db.finishers.update(
            {"_id": ObjectId(finisher_id)},
            {"$push": {"votes": form.vote.data}})
        return redirect(url_for("display_finisher", finisher_id=finisher_id))

    return render_template("finisher.html", finisher=finisher, rating=rating,
                           categories=categories, form=form, reviews=reviews)


# browse view so user can see all finishers posted by everyone
@app.route("/browse_finishers")
@login_required
def browse_finishers():
    finishers = list(mongo.db.finishers.find())
    categories = list(mongo.db.categories.find())

    return render_template(
        "browse_finishers.html", finishers=finishers, categories=categories)


# page for admin user to add new exercises to database
@app.route("/add_exercises", methods=["GET", "POST"])
@login_required
def add_exercises():
    form = add_exercise()
    if current_user.is_admin:
        if form.validate_on_submit():
            exercise = {
                form.exercise_name.data: None
            }
            flash("Exercise added to database")
            mongo.db.exercises.insert_one(exercise)
            return redirect(url_for("add_exercises"))

    return render_template("add_exercises.html", form=form)


@app.route("/autofill", methods=["GET", "POST"])
def autofill():
    if request.method == 'GET':
        message = list(mongo.db.exercises.find({}, {'_id': False}))
        return jsonify(message)


@app.route("/logout")
@login_required
def logout():
    flash("You have been logged out")
    logout_user()
    return redirect(url_for("login"))


@app.errorhandler(401)
def user_not_logged_in(e):
    flash("Please log in to access that page")
    return redirect(url_for("login"))


@app.errorhandler(404)
def error_404(e):
    return render_template("error_404.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
