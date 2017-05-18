__all__ = ['Post']

from application import db
import datetime


class Post(db.Model):

    # The unique primary key for each post created.
    id = db.Column(db.Integer, primary_key=True)

    # The free-form text-based content of each post.
    content = db.Column(db.Text())

    #  The date/time that the post was created on.
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow,
        index=True)

    # The user ID that created this post.
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body

    def __init__(self, user_id, content):
        """Initialize a new Post object."""

        self.user_id = user_id
        self.content = content
