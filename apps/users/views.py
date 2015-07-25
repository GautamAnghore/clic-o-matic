from flask import render_template, request, redirect, url_for

from apps.users import users
from forms import *

from apps import database
from apps import Sessions
from apps import login_required

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
                return redirect(url_for('users.add_page'))
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
                return redirect(url_for('dashboard.dashboard_index'))
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
@login_required
def logout(username):

    if sessions.pop_username(username) is True:
        return redirect(url_for('master.index'))
    else:
        # flag : stage 3
        # flag : bug [ alert cannot logout ]
        return redirect(url_for('dashboard.dashboard_index'))


@users.route('/addpage', methods=['GET', 'POST'])
@login_required
def add_page():
    if request.method == 'POST':
        # submit
        form = AddPageForm(request.form)

        if form.validate():
            status = user.add_page_db(sessions.logged_in(), form.pageurl.data)

            if status:
                return redirect(url_for('dashboard.dashboard_index', url=form.pageurl.data))
            else:
                # flag : stage 3
                # add something like alert.error('some error, cannot add')
                return render_template('addpage.html', form=form, user=sessions.logged_in())

        else:
            # flag : stage 3
            # alert.error('Please Provide Appropriate Details')
            return render_template('addpage.html', form=form, user=sessions.logged_in())
    else:
        return render_template('addpage.html', form=AddPageForm(), page_domain=url_for('master.index', _external=True), user=sessions.logged_in())
