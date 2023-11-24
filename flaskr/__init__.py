import os
from flask import Flask
from flask.views import View

#"the application factory function"
def create_app(test_config = None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True) #creates the Flask instance
    app.config.from_mapping(
        SECRET_KEY='dev',
        #used by Flask and extensions to keep data safe
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
        #path where database file will be saved
    )

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    #For db.py
    from . import db
    db.init_app(app)

    #For auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    #For blog.py
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    #For profile.py (My attempt at understanding Flask)
    from . import profile
    app.register_blueprint(profile.bp)
    profile.init_app(app)
    
    #Some authentication views referred to a plain index endpoint.
    # .add_url_rule associates the endpoint name 'index' with the 
    # '/' url so that url_for('index') or url_for('blog.index') will both work,
    # generating the same '/' URL either way.

    return app