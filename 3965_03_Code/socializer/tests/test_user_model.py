from application.users import models


def test_create_user_instance(session):
    """Create and save a user instance."""

    email = 'test@example.com'
    username = 'test_user'
    password = 'foobarbaz'

    user = models.User(email, username, password)
    session.add(user)
    session.commit()

    # We clear out the database after every run of the test suite,
    # but the order of tests may affect which ID is assigned.
    # Let's not depend on magic numbers in tests if we can avoid it.
    assert user.id is not None
    assert user.id >= 1

    assert user.followed.count() == 0
    assert user.newsfeed().count() == 0


def test_user_relationships(session):
    """User following relationships."""

    user_1 = models.User(
        email='test1@example.com', username='test1',
        password='foobarbaz')
    user_2 = models.User(
        email='test2@example.com', username='test2',
        password='bingbarboo')

    session.add(user_1)
    session.add(user_2)

    session.commit()

    assert user_1.followed.count() == 0
    assert user_2.followed.count() == 0

    user_1.follow(user_2)

    assert user_1.is_following(user_2) is True
    assert user_2.is_following(user_1) is False
    assert user_1.followed.count() == 1

    user_1.unfollow(user_2)

    assert user_1.is_following(user_2) is False
    assert user_1.followed.count() == 0
