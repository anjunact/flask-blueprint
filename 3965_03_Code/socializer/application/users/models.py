__all__ = ['followers', 'User']

import datetime
from application import db, flask_bcrypt, user_followed
from ..posts.models import Post


# We use the explicit SQLAlchemy mappers for declaring the followers table,
# since it does not require any of the features that the declarative base
# model brings to the table.
#
# The `follower_id` is the entry that represents a user who *follows* a
# `user_id`.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'),
        primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),
        primary_key=True))


class User(db.Model):

    # The primary key for each user record.
    id = db.Column(db.Integer, primary_key=True)

    # The unique email for each user record.
    email = db.Column(db.String(255), unique=True)

    # The unique username for each record.
    username = db.Column(db.String(40), unique=True)

    # The hashed password for the user
    password = db.Column(db.String(60))

    #  The date/time that the user account was created on.
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    followed = db.relationship('User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.user_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

    def __init__(self, email, username, password):
        """Initialize the user object with the required attributes."""

        self.email = email
        self.username = username
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        """All our registered users are authenticated."""
        return True

    def is_active(self):
        """All our users are active."""
        return True

    def is_anonymous(self):
        """We don't have anonymous users; always False"""
        return False

    def get_id(self):
        """Get the user ID."""
        return unicode(self.id)

    def unfollow(self, user):
        """
        Unfollow the given user.

        Return `False` if the user was not already following the user.
        """

        if not self.is_following(user):
            return False

        self.followed.remove(user)
        return self

    def follow(self, user):
        """
        Follow the given user.

        Return `False` if the user was already following the user.
        """

        if self.is_following(user):
            return False

        self.followed.append(user)

        # Publish the signal event
        user_followed.send(self)

        return self

    def is_following(self, user):
        """
        Returns boolean `True` if the current user is following the given `user`,
        and `False` otherwise.
        """
        followed = self.followed.filter(followers.c.user_id == user.id)
        return followed.count() > 0

    def newsfeed(self):
        """
        Return all posts from users followed by the current user,
        in descending chronological order.

        """

        join_condition = followers.c.user_id == Post.user_id
        filter_condition = followers.c.follower_id == self.id
        ordering = Post.created_on.desc()

        return Post.query.join(followers,
                (join_condition)).filter(filter_condition).order_by(ordering)
