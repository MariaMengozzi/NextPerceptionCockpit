import json
from numpy import False_
from project import app
from flask import render_template, redirect, url_for, request, session
import pandas as pd
from project.models.Model_profile import Model_profile
from project.models.Model_activity import Model_activity
from project.models.Model_challenges import Model_challenges

from project.models.auth_decorator import login_required

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        print(request.form["nick"]) #quando siamo sul profilo di un altro dobbiamo prendere il suo nick
        nick = request.form["nick"]
    else: 
        nick =  dict(session).get('nickname', None)
    
    friends = Model_profile.get_friends(nick)
    ftd_score = 0
    activities = {}
    for activity  in Model_profile.get_personal_activities(nick):
        if activity['id_attivita'] is not None:
            activities[activity['id_attivita']] = {
                'img' : Model_profile.get_profile_image(nick),
                        'nick': nick,
                        'data': activity['data'],
                        'ftd_score' : str(round(activity['ftd'] * 100, 2))+'%',
                        'eco_score' : '60%',
                        'ftd_res' : Model_activity.get_results_activity(int(activity['id_attivita'])),
                        'eco_res' : [],
                        'like' : Model_activity.get_likes_number(activity['id_attivita'])
            }

    result_of_last_10d = pd.DataFrame(json.loads(Model_profile.get_element_and_ftd_group_by_days(nick, False)))
    ongoing, finished = Model_challenges.get_filtered_challenges()
    
    info = {
            'img' : Model_profile.get_profile_image(nick), 
            'nick': nick,
            'just_friend': True if request.method != 'POST' else Model_profile.are_friends(dict(session).get('nickname', None), nick),
            'ftd_score' : str(round(result_of_last_10d['ftd'].mean()*100, 2)) + '%' if len(activities) != 0 else 0,
            'eco_score' : '55%',
            'livello' : round(result_of_last_10d['ftd'].mean()*100/20) if len(activities) != 0 else 0, #calcolalo dalla media del FTD come mean int(ftd/20) --> FTD : 100 = x : 5
            'friends': len(friends),
            'friends_list' : friends,
            'total_savings': 200,
            'ongoing_challenges': ongoing,
            'finished_challenges':finished,
            'activities' : activities
        }

    data = {
        "title": "Profilo",
        "name": "profile.html",
        "first": False,
        "info": info
    }

    return render_template('base.html', data = data)

@app.route('/add_friend', methods = ['GET', 'POST'])
@login_required
def add_friend():
    return str(Model_profile.insert_follower(dict(session).get('nickname', None), request.form["nick"]))

@app.route('/get_elementOfDistraction_data', methods=['POST'])
@login_required
def get_elementOfDistraction_data():
    data = Model_profile.get_element_and_ftd(request.form["nick"])
    return data

@app.route('/get_last_10_FTD', methods=['POST'])
@login_required
def get_last_10_FTD():
    data = Model_profile.get_element_and_ftd_group_by_days(request.form["nick"],True)
    return data
