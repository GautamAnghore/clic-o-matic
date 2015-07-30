from flask import render_template, redirect, url_for
from apps import master
from apps import Sessions

sessions = Sessions()

@master.route('/')
def index():
    if sessions.logged_in() is not None:
        return redirect(url_for('dashboard.dashboard_index'))

    return render_template("home.html")
