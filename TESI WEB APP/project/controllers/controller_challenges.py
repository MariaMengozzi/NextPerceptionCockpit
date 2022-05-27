from project import app
from flask import render_template, redirect, url_for, request, session
"""
    Import Models
from project.models.Model_example import Model_example
"""

from project.models.auth_decorator import login_required
from project.models.Model_challenges import Model_challenges

#route index
@app.route('/challenges', methods = ['GET', 'POST'])
@login_required
def challenges():



    data = {
        "title": "Challenges",
        "name": "challenges.html",
        "first": False,
        'challenges': Model_challenges.get_all_challenges()
    }

    return render_template('base.html', data = data)