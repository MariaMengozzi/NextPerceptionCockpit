from project import app
from flask import render_template, redirect, url_for, request, session
import json

from project.models.Model_notification import Model_notification
    
from project.models.auth_decorator import login_required
#route index
@app.route('/notification', methods = ['GET'])
@login_required
def notification():
    notification = Model_notification.get_user_notifications(dict(session).get('nickname', None))#[[1, '2021-02-14', 'notifica 1', True], [2,'2021-02-15', 'notifica 2', False], [3,'2021-02-16', 'notifica 3', False]]
    data = {
        "title": "Notification",
        "name": "notification.html",
        "first": False,
        "notification": notification
    }
    return render_template('base.html', data = data)

@app.route('/read_notification', methods = ['POST'])
@login_required
def read_notification():
    id_notification = request.form["id_notification"]
    state = Model_notification.update_notification(int(id_notification))
    '''if state:
        print('update corretto della notifica')
    else: 
        print('errore nell\'update della notifica') '''
    return str(state)

@app.route('/update_notification', methods = ['POST'])
@login_required
def update_notification():
    notification_list = Model_notification.get_user_notifications(dict(session).get('nickname', None))
    res = {
        'count': len(notification_list),
        'notifications_list' : notification_list
    }
    return json.dumps(res)
       
