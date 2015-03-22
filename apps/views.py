from flask import render_template
from apps import master


@master.route('/')
def index():
    return render_template("home.html")
