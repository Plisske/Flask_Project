from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from markupsafe import escape
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import click

import requests
import json




bp = Blueprint('profile',__name__,url_prefix='/profile')

def init_app(app):
    app.cli.add_command(init_get_apod)
    #adds a new command that can be called with the flask command

class APOD_api():

    def __init__(self, title, explanation, image_url, copyright=''):
        self.title = title
        self.explanation = explanation
        self.image_url = image_url
        self.copyright = copyright

    def __repr__(self):
        return f"{self.title} - {self.explanation}"

my_APOD : APOD_api

@bp.route('/about')
def about():
    return render_template('profile/about.html')

@bp.route('/projects/')
def projects():
    return render_template('profile/project.html')


def get_APOD():
    response = requests.get('https://api.nasa.gov/planetary/apod?api_key='+My_API_key)
    if response.status_code == 200:
        r = response.json()
        if r['copyright'] == None:
            r['copyright'] = ''
        my_APOD = APOD_api(r['title'],r['explanation'],r['url'],r['copyright']) #Return this object into a container of some sort
        db = get_db()
        db.execute(
                'INSERT INTO APOD_api (title, explanation, image_url, copyright)'
                ' VALUES (?, ?, ?, ?)',
                (my_APOD.title, my_APOD.explanation, my_APOD.image_url, my_APOD.copyright)
        )
        db.commit()

@click.command('get-apod')
def init_get_apod():
    get_APOD()
    click.echo('Successfully obtained APOD.')


@bp.route('/api_things/')
def api_things():#Plug My_APOD container into here and use javascript or something apparently.
    return render_template('profile/api_things.html', variable=my_APOD)
