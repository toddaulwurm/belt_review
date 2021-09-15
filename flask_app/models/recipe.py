from re import M
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.thirty_min = data["thirty_min"]
        self.made_at = data["made_at"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user = {}


    

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data["name"]) < 2:
            flash("Name must be greater than 2 characters")
            is_valid = False
        if len(form_data["description"]) < 2:
            flash("Description must be greater than 2 characters")
            is_valid = False
        if len(form_data["instructions"]) < 2:
            flash("Instructions must be greater than 2 characters")
            is_valid = False
        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, thirty_min, made_at, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(thirty_min)s, %(made_at)s, NOW(), NOW(), %(user_id)s);"

        results = connectToMySQL("recipes_schema").query_db(query, data)
        return results

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = user_id"
        results = connectToMySQL("recipes_schema").query_db(query)

        all_recipes = []

        for row in results: 
            recipe = cls(row)

            user_data = {
                "id" : row["id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["created_at"],
                "updated_at" : row["updated_at"],
            }
            recipe.user = user.User(user_data)
            all_recipes.append(recipe)

        return all_recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = user_id WHERE recipes.id = %(recipe_id)s"

        results = connectToMySQL("recipes_schema").query_db(query, data)

        recipe = cls(results[0])

        user_data = {
            "id" : results[0]["id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["created_at"],
            "updated_at" : results[0]["updated_at"],
        }
        recipe.user = user.User(user_data)

        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description =  %(description)s, instructions = %(instructions)s, thirty_min = %(thirty_min)s, made_at = %(made_at)s, updated_at = NOW() WHERE id = %(recipe_id)s;"

        results = connectToMySQL("recipes_schema").query_db(query, data)

        return

    @classmethod
    def delete(cls, data):
        query= "DELETE FROM recipes WHERE id = %(recipe_id)s;"

        results = connectToMySQL("recipes_schema").query_db(query, data)

        return