from flask import Flask, Blueprint, render_template, request

auth = Blueprint("auth", __name__, template_folder="templates")

@auth.route("/", methods=['POST', 'GET'])
@auth.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        
    return render_template("index.html", exercise=exercise, weight=weight, reps=reps)


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        return render_template("signup.html")