from flask import Blueprint, render_template, url_for, redirect, flash, g, current_app
from flask.ext.login import login_user, logout_user

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from sqlalchemy import exc

from models import User
from application import db, flask_bcrypt

users = Blueprint('users', __name__, template_folder='templates')


class CreateUserForm(Form):
    """
    Encapsulate the necessary information required for creating a new user.
    """

    username = StringField('username', validators=[DataRequired(), Length(min=3, max=40)])
    email = StringField('email', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('password', validators=[DataRequired(),
        Length(min=8)])


class LoginForm(Form):
    """
    Represents the basic Login form elements & validators.
    """

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),
        Length(min=6)])


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Basic user creation functionality.

    """

    form = CreateUserForm()

    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            # A unique column constraint was violated
            current_app.exception("User unique constraint violated.")
            flash("User already exists!")
            return render_template('users/signup.html', form=form)
        except exc.SQLAlchemyError:
            current_app.exception("Could not save new user!")
            flash("Something went wrong while creating this user!")
            return render_template('users/signup.html', form=form)

            # Once we have persisted the user to the database successfully,
            # authenticate that user for the current session
            login_user(user, remember=True)
            return redirect(url_for('users.index'))

    return render_template('users/signup.html', form=form)


@users.route('/', methods=['GET'])
def index():
    return "User index page!", 200


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
        return redirect(url_for('users.index'))

    form = LoginForm()

    if form.validate_on_submit():

        # We use one() here instead of first()
        user = User.query.filter_by(username=form.username.data).one()

        if not user or not flask_bcrypt.check_password_hash(user.password,
                form.password.data):

            flash("No such user exists.")
            return render_template('users/login.html', form=form)

        login_user(user, remember=True)
        return redirect(url_for('users.index'))

    return render_template('users/login.html', form=form)


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('users.login'))
