import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
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
csrf = CSRFProtect(app)
csrf.init_app(app)

mongo = PyMongo(app)


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)


@login_manager.user_loader
def load_user(user_id):
    user_obj = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_obj)


class registration_form(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class login_form(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


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
            "password": generate_password_hash(form.password.data)
        }
        session["user"] = form.username.data.lower()
        mongo.db.users.insert_one(new_user)
        return redirect(url_for("browse_finishers"))

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
                session["user"] = form.username.data.lower()
                loginUser = User(username_exists)
                login_user(loginUser)
                return redirect(url_for("dashboard", username=session["user"]))

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
    username = mongo.db.users.find_one({
        "username": session["user"]})["username"]

    if session["user"]:
        return render_template("dashboard.html", username=username)

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
        # sort form_input_nested into an array of objects
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
            "created_by": session["user"]
        }
        mongo.db.finishers.insert_one(finisher)
        return redirect(url_for("browse_finishers"))
    return render_template(
        "add_finisher.html", categories=categories)


# Allow a user to edit a finisher and add to their library
@app.route("/edit_finisher/<finisher_id>", methods=["GET", "POST"])
@login_required
def edit_finisher(finisher_id):
    finisher = mongo.db.finishers.find_one({"_id": ObjectId(finisher_id)})
    categories = mongo.db.categories.find()
    return render_template(
        "edit_finisher.html", finisher=finisher, categories=categories)


# browse view so user can see all finishers posted by everyone
@app.route("/browse_finishers")
@login_required
def browse_finishers():
    finishers = list(mongo.db.finishers.find())
    categories = list(mongo.db.categories.find())
    return render_template(
        "browse_finishers.html", finishers=finishers, categories=categories)


@app.route("/logout")
@login_required
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    logout_user()
    return redirect(url_for("login"))


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


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
