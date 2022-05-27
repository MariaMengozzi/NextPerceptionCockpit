from flask.globals import request
from project import app
from flask import render_template, redirect, url_for, session

from authlib.integrations.flask_client import OAuth

'''Import Models'''
from project.models.Model_first_page import Model_first_page


app.secret_key = '8f42a73054b1749f8f58848be5e6502c' #da cambiare

#oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='354392123560-jn6eg0fn5h4eeecg99ojru6vt4f40qem.apps.googleusercontent.com',
    client_secret='QfC3_X4rTQbXe0egekO8Vx3U',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    #userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    prompt='consent' #permette di richiedere il login ogni volta
)

""" @app.route('/')
#@login_required --> https://github.com/Vuka951/tutorial-code/blob/master/flask-google-oauth2/ è in oauth decorator
def hello_world():
    #email = dict(session)['profile']['email']
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as {email}!' """

type_of_enter = ''

#route index
@app.route('/')
def first_page():
    data = {
        "title": "First page",
        "name": "first_page.html",
        "first": True,
        "errorLogin" : False,
        "errorSignUp" : False
    }
    session.clear()
    return render_template('base.html', data = data)


@app.route('/login', methods=['GET','POST'])
def login_user():
    global type_of_enter
    type_of_enter = 'login'
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    if(dict(session).get('email', None) == None) :
        return google.authorize_redirect(redirect_uri)
    else:
        return redirect('/')

@app.route('/signUp', methods=['GET','POST'])
def signUp_user():
    global type_of_enter
    type_of_enter = 'sign_up'
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    if(dict(session).get('email', None) == None) :
        return google.authorize_redirect(redirect_uri)
    else:
        return redirect('/')

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile

    if type_of_enter == 'login':
        #check if user is registered
        if Model_first_page.is_registered(user_info["email"].replace('@gmail.com', '')) > 0:
            session['email'] = user_info['email']
            session['new_user'] = False
            session['nickname'] = Model_first_page.get_user_nickname(user_info['email'])
            session['picture'] = user_info["picture"]
            return redirect('/welcome')
        else:
            print('errore login, utente non registrato')
            data = {
                "title": "First page",
                "name": "first_page.html",
                "first": True,
                "errorLogin" : True,
                "errorSignUp" : False
            }
            session.clear() #lo devo fare altrimenti rimangono i dati 
            return render_template('base.html', data = data)
    else:
        #insert into db new user
        session['new_user'] = True

        session['email'] = user_info['email']
        session['picture'] = user_info["picture"]
        session['nickname'] = user_info["email"].replace('@gmail.com', '')
        return_state = Model_first_page.insert_new_user(user_info['email'], user_info["email"].replace('@gmail.com', ''), user_info["picture"])
        if return_state: 
            print('inserimento avvenuto correttamente')
            return redirect('/welcome')
        else:
            print('errore inserimento')
            data = {
                "title": "First page",
                "name": "first_page.html",
                "first": True,
                "errorLogin" : False,
                "errorSignUp" : True
            }
            session.clear() #lo devo fare altrimenti rimangono i dati 
            return render_template('base.html', data = data)

@app.route('/logout')
def logout_user():
    for key in list(session.keys()):
        session.pop(key)
    print(dict(session).get('email', None))
    return redirect('/')