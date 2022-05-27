from project import app
from flask import render_template, redirect, url_for, request, session

from project.models.Model_ranking import Model_ranking


from project.models.auth_decorator import login_required

#route index
@app.route('/ranking', methods = ['GET','POST'])
@login_required
def global_ranking():
    global_ranking = Model_ranking.get_ranking()
    if len(global_ranking) < 10:
        mancanti = 10-len(global_ranking)
        for item in range(mancanti):
            global_ranking.append(('','-'))
    data = {
        "title": "Ranking",
        "name": "ranking.html",
        "first": False,
        "global_ranking": global_ranking
    }
    return render_template('base.html', data = data)