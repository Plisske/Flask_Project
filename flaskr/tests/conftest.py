import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__),'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    #Creates and opens a temporary file, returning the file descriptor and
    # path to it. The DATABASE Path is overridden so it poitns to this
    # temporary path instead of the instance folder. Removed after the test is done.

    app = create_app({
        'TESTING':True,
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()
#calls app.test_client() with the application object created by the app fixture.
#Tests will use the client to make requests to the application without running the server.

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
#Creates a runner that can call the Click commands registered with the application

#Pytest uses fixtures by matching their function names with
# the names of arguments in the test functions.

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self,username='test',password='test'):
        return self._client.post(
            '/auth/login',
            data={'username':username,'password':password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)
#With the auth fixture, you can call auth.login() in a test to log in
# as the 'test' user, which was inserted as part of the test data in the app fixture.



