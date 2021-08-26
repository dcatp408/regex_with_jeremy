import re
from flask.wrappers import Request
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.saved_regular_expressions import Expression
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def login():
    session["regular_expression"] = ""
    session["test_string"] = ""
    return render_template("login.html")


@app.route("/login_user", methods=["POST"])
def login_user():
    data = {"username": request.form["username"]}
    user_in_db = User.get_by_username(data)
    if not user_in_db:
        flash("Account doesn't exist", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Account doesn't exist", "login")
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/register_user", methods=["POST"])
def register_user():
    if User.register_validate(request.form) == False:
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username": request.form["username"],
        "password": pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/dashboard")


@app.route("/guest/dashboard")
def guest_user():
    return render_template("guest_dashboard.html")


@app.route("/delete_session")
def delete_session():
    if "user_id" not in session:
        return redirect("/")
    session.clear()
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    context = {
        "user": User.get_one(session["user_id"]),
        "expressions": Expression.get_all_expressions_for_one_user(session["user_id"])
    }
    print("*"*80)
    print(context["expressions"])
    print("*"*80)
    return render_template("dashboard.html", **context)


@app.route("/copy/expression/<int:id>")
def copy_expression(id):
    if "user_id" not in session:
        return redirect("/")
    if Expression.get_one(id) == False:
        return redirect("/")
    if Expression.get_one(id).user_id != session["user_id"]:
        return redirect("/")
    session["regular_expression"] = Expression.get_one(id).regular_expression
    session["test_string"] = Expression.get_one(id).test_string
    return redirect("/dashboard")


@app.route("/delete/expression/<int:id>")
def delete_expression(id):
    if "user_id" not in session:
        return redirect("/")
    if Expression.get_one(id) == False:
        return redirect("/")
    if Expression.get_one(id).user_id != session["user_id"]:
        return redirect("/")
    data = {"id": id,
            "regular_expression": "regular_expression",
            "test_string": "test_string",
            "user_id": "user_id"
            }
    Expression.delete(data)
    return redirect("/dashboard")


@ app.route("/clear/text", methods=["POST"])
def clear_text():
    session["regular_expression"] = ""
    session["test_string"] = ""
    if "user_id" not in session:
        return redirect("/guest/dashboard")
    else:
        return redirect("/dashboard")


@ app.route("/save", methods=["POST"])
def save():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "regular_expression": session['regular_expression'],
        "test_string": session['test_string'],
        "user_id": session['user_id']
    }
    if Expression.save_expression_validation(data) == False:
        return redirect("/dashboard")
    Expression.save(data)

    return redirect("/dashboard")


@ app.route("/match", methods=["POST"])
def match():

    regular_expression = request.form["regular_expression"]
    session["regular_expression"] = regular_expression
    regular_expression = re.compile('.*({}).*'.format(regular_expression))
    # print("*"*80)
    # print(regular_expression)
    # print("*"*80)
    test_string = request.form["test_string"]
    session["test_string"] = test_string
    is_valid = regular_expression.match(test_string)
    # print(is_valid)
    # print("*"*80)

    if is_valid == None:
        session["valid"] = False
    else:
        session["valid"] = True
    if "user_id" not in session:
        return redirect("/guest/dashboard")
    else:
        return redirect("/dashboard")


# @app.route("/search", methods=["POST"])
# def search():
#     regular_expression = request.form["regular_expression"]
#     # print("*"*80)
#     # regular_expression= r"'^c./t+$"
#     regular_expression = re.compile('.*({}).*'.format(regular_expression))
#     print("*"*80)
#     print(regular_expression)
#     print("*"*80)
#     test_string = request.form["test_string"]
#     is_valid = regular_expression.search(test_string)
#     print(is_valid)
#     print("*"*80)
#     if is_valid == None:
#         session["valid"] = False
#     else:
#         session["valid"] = True
#     return redirect("/dashboard")
