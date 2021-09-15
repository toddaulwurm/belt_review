import re
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.recipe import Recipe 

@app.route("/recipes/new")
def new_recipe():
    if 'user_id' not in session:
        flash("Please Login")
        return redirect("/")
    user_id = session["user_id"]
    return render_template("new_recipe.html", user_id = user_id)

@app.route("/validate_recipe", methods=['POST'])
def validate_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")

    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "thirty_min" : request.form["thirty_min"],
        "made_at" : request.form["made_at"],
        "user_id" : request.form["user_id"]
    }
    Recipe.create_recipe(data)
    return redirect("/dashboard")

@app.route("/recipes/<int:recipe_id>")
def show_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please Login")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    logged_in_id = session["user_id"]
    return render_template("show_recipe.html", recipe=recipe, logged_in_id = logged_in_id)


@app.route("/recipes/edit/<int:recipe_id>")
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        flash("Please Login")
        return redirect("/")
    data = {
        "recipe_id" : recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/update/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/{recipe_id}")
    data = {
        "recipe_id" : recipe_id,
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "thirty_min" : request.form["thirty_min"],
        "made_at" : request.form["made_at"],
    }
    Recipe.update_recipe(data)
    return redirect("/dashboard")

@app.route("/delete/<int:recipe_id>")
def delete(recipe_id):
    data = {
        "recipe_id" : recipe_id
    }
    Recipe.delete(data)
    return redirect("/dashboard")