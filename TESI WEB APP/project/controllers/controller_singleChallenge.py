from project import app
from flask import render_template, redirect, url_for, request, session

from project.models.Model_challenges import Model_challenges

# decorator for routes that should be accessible only by logged in users
from project.models.auth_decorator import login_required

#route index
@app.route('/single_challenge', methods = ['GET','POST'])
@login_required
def single_challenge():
    id_challenge = int(request.form['idChallenge'])
    challenge_ranking = Model_challenges.get_ranking_challenge(id_challenge)
    
    if len(challenge_ranking) < 10:
        mancanti = 10-len(challenge_ranking)
        for item in range(mancanti):
            challenge_ranking.append(('','-'))
            

    challenge = Model_challenges.get_challenge_info(id_challenge) #presa dal valore di post

    data = {
        "title": "single_challenge",
        "name": "single_challenge.html",
        "first": False,
        "challenge_ranking": challenge_ranking,
        "challenge" : challenge
    }
    return render_template('base.html', data = data)