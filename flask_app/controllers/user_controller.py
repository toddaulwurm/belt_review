from flask_app.models.recipe import Recipe
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    data = {
        "user_id" : session['user_id']
    }

    user = User.get_user_info(data)
    recipes = Recipe.get_all_recipes()
    return render_template("dashboard.html", user = user, recipes = recipes)


@app.route('/register', methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.register_user(data)
    session['user_id'] = user_id
    return redirect("/dashboard")



@app.route('/login_user', methods=['POST'])
def login_user():
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)

    validata = {
        "user" : user_in_db,
        "password" : request.form['password']
    }

    if not User.validate_login(validata):
        return redirect("/")

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")




@app.route("/")
def dummy():
    return redirect("/login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")