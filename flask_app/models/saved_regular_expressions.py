import flask_app
from flask_app.models.user import User
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
    def get_all(cls):
        query = "SELECT * FROM saved_regular_expressions;"
        results = connectToMySQL(DATABASE).query_db(query)
        expressions = []
        for expression in results:
            expressions.append(cls(expression))
        return expressions

    @classmethod
    def delete(cls, data):
        query = "delete from saved_regular_expressions where id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
