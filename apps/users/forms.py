from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Length, EqualTo, Email


class SignupForm(Form):

    username = TextField('Username',
                         validators=[Required('Please provide username'),
                                     Length(min=3, message=('Please provide a Longer username'))])

    password = PasswordField('Password',
                             validators=[Required('Please provide a password'),
                                         Length(min=5, message=('Please provide a Longer password ')),
                                         EqualTo('confirm', message=('Passwords must match'))])

    confirm = PasswordField('Confirm Password',
                            validators=[Required('Please Confirm the password')])

    email = TextField('Email',
                      validators=[Email('Not a valid mail address')])
