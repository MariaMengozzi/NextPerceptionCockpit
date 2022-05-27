from flask import Flask, jsonify, render_template, request, session, url_for, redirect
from database.database_manager import Database
from authlib.integrations.flask_client import OAuth



app = Flask(__name__)
app.config.from_object(__name__)
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

@app.route('/')
def home():
    return render_template("CarHome.html")

#non è presente il login del'auto perchè sarà di default inserito al momento dell'installzione dell'applicazione nella macchina
@app.route('/login', methods=['GET'])
def login_user():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    if(dict(session).get('email', None) == None) :
        return google.authorize_redirect(redirect_uri)
    else:
        return redirect('/cockpit')

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    resp.raise_for_status()
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/cockpit')

@app.route('/logout')
def logout_user():
    for key in list(session.keys()):
        session.pop(key)
    print(dict(session).get('email', None))
    return redirect('/')


@app.route('/cockpit')
def cockpit():
    #app.route('/cockpit')
    email = dict(session).get('email', None)
    print(email)
    return render_template("CarCockpit.html")

@app.route('/get_cockpit_data')
def get_cockpit_data():
    data = db.get_cockpit_data()
    return data

@app.route('/infotainment')
def infotainmet():
    #app.route('/infotainment')
    return render_template("CarInfotainment.html")

@app.route('/get_elementOfDistraction_data')
def get_elementOfDistraction_data():
    data = db.get_elementOfDistraction_data()
    return data

if __name__ == "__main__":
    db = Database()
    app.run(use_reloader=False, port=8000, debug=True)
