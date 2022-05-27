  
"""
    Example Controllers
"""

from project import app
from flask import render_template, redirect, url_for

'''Import Models'''
from project.models.Model_example import Model_example

#route index
@app.route('/example', methods = ['GET'])
def index():
    prova = Model_example.get_prova()
    testo = prova.text
    prova.get_row()
    data = {
        "title": "Hello World",
        "body": testo #"Flask simple MVC"
    }
    return render_template('index.html', data = data)#index.html è in templates

