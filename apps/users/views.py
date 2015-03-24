from flask import render_template, request, redirect, url_for

from apps.users import users
from forms import *

from apps import database
from apps import Sessions

import db

user = db.User(database)
sessions = Sessions()


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
                sessions.push_username(form.username.data)
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
        if sessions.logged_in() is not None:
            # flag : stage 3
            # flag : bug [ return to dashboard, alert already signed in ]
            return redirect(url_for('master.index'))
        else:
            # show the form to signup
            return render_template('signup.html', form=SignupForm())


@users.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        form = LoginForm(request.form)

        if form.validate():
            loggedin = user.check_user(form.username.data, form.password.data)

            if loggedin is not None:
                sessions.push_username(form.username.data)
                # flag : stage 1
                # flag : bug [ add user to session ]
                return "Logged In"
            else:
                # flag : stage 2
                # add something like alert.error('Wrong Credentials')
                return render_template('login.html', form=form)

        else:
            # flag : stage 2
            # alert.error('Please Provide Appropriate Details')
            return render_template('login.html', form=form)
    else:
        if sessions.logged_in() is not None:
            # flag : stage 3
            # flag : bug [ return to dashboard, alert already signed in ]
            return redirect(url_for('master.index'))
        else:
            return render_template('login.html', form=LoginForm())


@users.route('/logout/<username>', methods=['GET'])
def logout(username):

    if sessions.pop_username(username) is True:
        return redirect(url_for('master.index'))
    else:
        # flag : stage 3
        # flag : bug [ alert cannot logout ]
        return redirect(url_for('dashboard.dashboard_index'))
