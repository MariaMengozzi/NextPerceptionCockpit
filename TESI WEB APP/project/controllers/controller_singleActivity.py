from numpy import integer
from project import app
from flask import render_template, redirect, url_for, request, session

from project.models.Model_activity import Model_activity


# decorator for routes that should be accessible only by logged in users
from project.models.auth_decorator import login_required


@app.route('/single_activity', methods = ['GET', 'POST'])
@login_required
def single_activity():
    id_activity = request.form["idActivity"]
    info =  Model_activity.get_info_from_id(int(id_activity))
    activity = {
            'id' : id_activity,
            'img' :Model_activity.get_image_from_activity(int(id_activity)), #dall'attività prendi il nick e seleziona l'immagine relativa
            'nick': info[0]['nickname'], #select from id_activity
            'data': info[0]['data'],
            'ftd_score' : '80%',
            'eco_score' : '55%',
            'ftd_res' : Model_activity.get_results_activity(int(id_activity)),
            #'distractionElement' : {'A': 20, 'B':30, 'C':50},
            'eco_res' : [],
            'eco_risparmio': '150€',
            'like' : Model_activity.get_likes_number(int(id_activity)),
            'has_like': Model_activity.has_like(int(id_activity), dict(session).get('nickname', None))
        }

    data = {
        "title": "Single activity",
        "name": "single_activity.html",
        "first": False,
        "activity": activity
    }

    return render_template('base.html', data = data)

@app.route('/set_like', methods = ['POST'])
@login_required
def set_like_to_activity():
    return str(Model_activity.set_like(int(request.form["idActivity"]), dict(session).get('nickname', None)))


@app.route('/get_elementOfDistraction_data_single_a', methods = ['POST'])
def get_elementOfDistraction_data_single_a():
    data =  Model_activity.get_elementOfDistraction_data(int(request.form["idActivity"]))
    return data

@app.route('/get_FTD_single_activity',methods = ['POST'])
def get_FTD_single_activity():
    data = Model_activity.get_FTD_single_activity(int(request.form["idActivity"]))
    return data
