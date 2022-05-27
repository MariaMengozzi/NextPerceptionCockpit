from project import app
from flask import render_template, redirect, url_for, request, session

    
from project.models.Model_home import Model_home
from project.models.Model_profile import Model_profile
from project.models.Model_activity import Model_activity


from project.models.auth_decorator import login_required

#route index
@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():

    nick =  dict(session).get('nickname', None)
    activities = {}
    for activity  in Model_home.get_activities(nick):
        if activity['id_attivita'] is not None:
            activities[activity['id_attivita']] = {
                'img' : Model_home.get_profile_image_from_nick(activity['nickname']),
                'nick': activity['nickname'],
                'data': activity['data'],
                'ftd_score' : str(round(activity['ftd'] * 100, 2))+'%',
                'eco_score' : '60%',
                'ftd_res' : Model_activity.get_results_activity(int(activity['id_attivita'])),
                'eco_res' : [],
                'like' : Model_activity.get_likes_number(activity['id_attivita'])
            }

    data = {
        "title": "Home",
        "name": "home_page.html",
        "first": False,
        "activities": activities
    }

    return render_template('base.html', data = data)