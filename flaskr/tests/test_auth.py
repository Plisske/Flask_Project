import pytest
from flask import g,session
from flaskr.db import get_db

def test_register(client,app):

    #To test that the page renders successfully, a simple request is made and checked
    # for a '200 OK' status_code. If rendering failed, 
    # Flask would return a '500 Internal Server Error' code.
    assert client.get('/auth/register').status_code == 200
    #client.get() makes a GET request and returns the Response object returned by Flask

    response = client.post(
        '/auth/register', data={'username':'a', 'password':'a'}
    )
    #client.post() makes a POST request, converting the data dict into form data.

    assert response.headers["Location"] =="/auth/login"
    #headers will have a Location header with the login URL 
    # when the register view redirects to the login view

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None
    
@pytest.mark.parametrize(('username','password','message'),(
    ('','',b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
    ))
#'pytest.mark.parametrize' tells Pytest to run the same test function
# with different arguments. You use it here to test different invalid input and
# error messages without writing the same code three times.

def test_register_validate_input(client,username,password,message):
    response = client.post(
        '/auth/register',
        data={'username':username,'password':password}
    )
    #'data' contains the body of the response as bytes. If you expect a certain
    # value to render on the page, check that it's in 'data'
    # Bytes must be compared to bytes. If you want to compare text, use get_data(as_text=True).
    assert message in response.data

#The tests for the 'login' view are very similar to those for register. Rather than testing the
# data in the database, 'session' shnould have 'user_id' set after loggin in.

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"]=="/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] =='test'


@pytest.mark.parametrize(('username','password','message'),(
    ('a','test',b'Incorrect username.'),
    ('test','a',b'Incorrect password.')
))

def test_login_validate_input(auth,username,password,message):
    response=auth.login(username,password)
    assert message in response.data

#Using 'client' in a 'with' block allows accessing context variables
# such as 'session' after the response is returned. Normally accessing
# 'session' outside of a request would raise an error.

def test_logout(client,auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

#Testing 'logout' is the opposite of 'login'. 
# 'session' should not contain 'user_id' after logging out


