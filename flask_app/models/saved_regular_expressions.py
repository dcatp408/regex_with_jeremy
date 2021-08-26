import flask_app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import app, flash


DATABASE = 'regex_database'


class Expression:
    def __init__(self, data):
        self.id = data['id']
        self.regular_expression = data['regular_expression']
        self.test_string = data['test_string']
        self.user_id = data["user_id"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO saved_regular_expressions (regular_expression, test_string, user_id) VALUES ( %(regular_expression)s, %(test_string)s , %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM saved_regular_expressions WHERE id = %(user_id)s;"
        data = {
            'user_id': id
        }
        results = connectToMySQL(DATABASE).query_db(query, data)
        users = []
        for user in results:
            users.append(cls(user))
        return users[0]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM saved_regular_expressions;"
        results = connectToMySQL(DATABASE).query_db(query)
        expressions = []
        for expression in results:
            expressions.append(cls(expression))
        return expressions

    @classmethod
    def get_all_expressions_for_one_user(cls, id):
        query = "SELECT * FROM saved_regular_expressions where user_id = %(user_id)s"
        data = {
            'user_id': id
        }
        results = connectToMySQL(DATABASE).query_db(query, data)

        expressions = []
        for expression in results:
            expressions.append(cls(expression))
        return expressions

    @classmethod
    def delete(cls, data):
        query = "delete from saved_regular_expressions where id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def save_expression_validation(data):
        is_valid = True
        print("*"*80)
        print("*"*80)
        if len(data["regular_expression"]) == 0:
            flash("Expression is required to save", "regular_expression")
            is_valid = False
        if len(data["test_string"]) == 0:
            flash("Test String is required to save", "test_string")
            is_valid = False
        return is_valid
