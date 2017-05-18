import datetime
import hashlib
from application import db


class Snap(db.Model):

    # The primary key for each snap record.
    id = db.Column(db.Integer, primary_key=True)

    # The name of the file; does not need to be unique.
    name = db.Column(db.String(128))

    # The extension of the file; used for proper syntax highlighting
    extension = db.Column(db.String(12))

    # The actual content of the snap
    content = db.Column(db.Text())

    # The unique, un-guessable ID of the file
    hash_key = db.Column(db.String(40), unique=True)

    #  The date/time that the snap was created on.
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow,
            index=True)

    # The user this snap belongs to
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('snaps', lazy='dynamic'))

    def __init__(self, user_id, name, content, extension):
        """Initialize the snap object with the required attributes."""

        self.user_id = user_id
        self.name = name
        self.content = content
        self.extension = extension

        # This could be made more secure by combining the application SECRET_KEY
        # in the hash as a salt.
        self.hash_key = hashlib.sha1(self.content + str(self.created_on)).hexdigest()

        self.created_on = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Snap %r>' % self.id
