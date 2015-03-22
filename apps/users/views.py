from flask import render_template, request

from apps.users import users
from forms import *


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # submit the form's data
        form = SignupForm(request.form)

        if form.validate():
            return "%s,%s,%s,%s" % (form.username.data, form.password.data, form.confirm.data, form.email.data)
        else:
            return render_template('signup.html', form=form)
    else:
        # show the form to signup
        return render_template('signup.html', form=SignupForm())
