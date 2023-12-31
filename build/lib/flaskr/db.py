import sqlite3

import click
from flask import current_app, g

def init_app(app):
    app.teardown_appcontext(close_db)
    #Tells Flask to call that function when cleaning up after returning the response
    app.cli.add_command(init_db_command)
    #adds a new command that can be called with the flask command

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
        #Establishes a connection to the file pointed at by the DATABASE configuration key    
            current_app.config['DATABASE'], 
            #Special object that points to the Flask application handling the request.
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        #Tells the connection to return rows that behave like dicts.
        #Allows accessing the columns by name.
    return g.db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    #returns a database connection, which is used to execute
    # the commands read from the file
    with current_app.open_resource('schema.sql') as f:
    #opens a file relative to the flaskr package
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
#Defines a command line command called init-db that calls the init_db() func
# and shows a success message to the user
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

