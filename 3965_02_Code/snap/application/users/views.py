from flask import Blueprint, flash, render_template, url_for, redirect, g
from flask.ext.login import login_user, logout_user

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

from models import User
from application import flask_bcrypt

users = Blueprint('users', __name__, template_folder='templates')


class LoginForm(Form):
    """
    Represents the basic Login form elements & validators.
    """

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),
        Length(min=6)])


@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    Basic user login functionality.

    If the user is already logged in (meaning we have a
    user object attached to the g context local), we
    redirect the user to the default snaps index page.

    If the user is not already logged in and we have
    form data that was submitted via POST request, we
    call the validate_on_submit() method of the Flask-WTF
    Form object to ensure that the POST data matches what
    we are expecting. If the data validates, we login the
    user given the form data that was provided and then
    redirect them to the default snaps index page.

    Note: Some of this may be simplified by moving the actual User
    loading and password checking into a custom Flask-WTF validator
    for the LoginForm, but we avoid that for the moment, here.
    """

    if hasattr(g, 'user') and g.user.is_authenticated():
        return redirect(url_for('snaps.listing'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not flask_bcrypt.check_password_hash(user.password,
                form.password.data):

            flash("No such user exists.")
            return render_template('users/login.html', form=form)

        login_user(user, remember=True)
        return redirect(url_for('snaps.listing'))

    return render_template('users/login.html', form=form)


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('snaps.listing'))
