import pytest
import os
from application import create_app, db as database

DB_LOCATION = '/tmp/test_app.db'


@pytest.fixture(scope='session')
def app():
    app = create_app(config='test_settings')
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(DB_LOCATION):
        os.unlink(DB_LOCATION)

    database.app = app
    database.create_all()

    def teardown():
        database.drop_all()
        os.unlink(DB_LOCATION)

    request.addfinalizer(teardown)
    return database


@pytest.fixture(scope='function')
def session(db, request):

    session = db.create_scoped_session()
    db.session = session

    def teardown():
        session.remove()

    request.addfinalizer(teardown)
    return session
