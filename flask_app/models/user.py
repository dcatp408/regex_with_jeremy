import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import app, flash
from flask_app.models.saved_regular_expressions import Expression

DATABASE = 'regex_database'


class User:
    def __init__(self, data):
        self.username = data['username']
        self.password = data['password']
        self.id = data["id"]
        self.saved_regular_expressions = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (username, password) VALUES ( %(username)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def update(cls, data):
    #     query = "update user set email = %(email)s, first_name =  %(first_name)s, last_name = %(last_name)s, updated_at = now() where id = %(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM user WHERE username = %(username)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result == False or len(result) == 0:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM user WHERE id = %(user_id)s;"
        data = {
            'user_id': id
        }
        results = connectToMySQL(DATABASE).query_db(query, data)
        users = []
        for user in results:
            users.append(cls(user))
        return users[0]

    @classmethod
    def delete(cls, data):
        query = "delete from user where id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def register_validate(data):
        is_valid = True
        if len(data["username"]) == 0:
            flash("Username is a required field", "username")
            is_valid = False
        elif len(data["username"]) < 2:
            flash("Username must have more than 2 characters", "username")
            is_valid = False
        else:
            username = User.get_by_username(data)
            if username != False:
                flash("Invalid Username", "username")
                is_valid = False

        if len(data["password"]) == 0:
            flash("Password is a required field", "password")
            is_valid = False
        elif len(data["password"]) < 5:
            flash("Password must be longer than 5 characters", "password")
            is_valid = False
        elif data["password"] != data["confirmpassword"]:
            flash("Passwords don't match", "password")
            is_valid = False
        return is_valid
