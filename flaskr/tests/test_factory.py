from flaskr import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING':True}).testing

#The argument below is what the pytest fixtures will match the functions with in conftest.
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'