__all__ = ['user_followed_email']

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def user_followed_email(user, **kwargs):
    logger.debug("Send an email to {user}".format(user=user.username))


from application import user_followed
user_followed.connect(user_followed_email)
