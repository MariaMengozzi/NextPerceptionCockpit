  
"""
    Example Controllers2
"""

from project import app
from flask import render_template, redirect, url_for, request
"""
    Import MOdels
from project.models.Model_example import Model_example
"""

@app.route('/secondPG', methods = ['POST','GET'])
def index2():
    #se il metodo == 'POST' usare request.form['name']
    if request.args.get('name') == None:
        data = {
            "title": "Hello World",
            "body": "Flask simple MVC"
        }
    else:
        data = {
            "title": request.args.get('name'),
            "body": "Flask simple MVC"
        }
    return render_template('index2.html', data = data)#index.html è in templates