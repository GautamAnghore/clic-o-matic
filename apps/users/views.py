from flask import render_template, request, redirect, url_for

from apps.users import users
from forms import *

from apps import database

import db

user = db.User(database)


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # submit the form's data
        form = SignupForm(request.form)

        if form.validate():
            # form validation success
            # can add to db
            if form.email.data != "":
                success = user.add_user(form.username.data,
                                        form.password.data,
                                        form.email.data)
            else:
                success = user.add_user(form.username.data,
                                        form.password.data)

            if success is True:
                # temperory
                # flag : bug stage 1
                return redirect(url_for(master.index))
            else:
                # to be changed with error handling
                # flag : feature
                # flag : bug [ if username exists, no proper msg given ]
                return "User creation failed, internal error"

        else:
            # form validation failed
            return render_template('signup.html', form=form)
    else:
        # get request
        # show the form to signup
        return render_template('signup.html', form=SignupForm())


@users.route('/login', methods=['GET', 'POST'])
def login():
    return "True"
