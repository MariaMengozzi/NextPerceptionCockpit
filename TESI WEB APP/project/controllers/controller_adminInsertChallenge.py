from random import random
from project import app
from flask import render_template, redirect, url_for, request, session
from datetime import datetime

# decorator for routes that should be accessible only by logged in users
from project.models.auth_decorator import login_required

from project.models.Model_challenges import Model_challenges



@app.route('/admin_insert_challenge', methods = ['GET','POST'])
@login_required
def admin_insert_challenge():

    if dict(session).get('nickname', None) == 'aftd26524': #email dell'aministratore
        data = {
        "title": "Admin Inser challenge",
        "name": "admin_insert_challenge.html",
        'today': datetime.today().strftime('%Y-%m-%d')
        }
        return render_template('admin_base.html', data = data)
    else :

        return redirect('/logout')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/insert_new_challenge', methods = ['POST'])
@login_required
def insert_new_challenge():
    #scarico l'immagine -> se da errore rimando alla home direttamente con l'errore, altrimenti faccio la insert
    status = 0
    if request.method == 'POST':
        # check if the post request has the file part
        if 'badge' not in request.files:
            return redirect('/welcome?error='+str(status))
        file = request.files['badge']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect('/welcome?error='+str(status))

        if file and allowed_file(file.filename):
            download_image_name = Model_challenges.save_image(file)
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
            nome, badge, data_i, data_f = request.form['nome_c'], download_image_name, request.form['data_i'], request.form['data_f']
    
    status = int(Model_challenges.insert_new_challenge(nome, badge, data_i, data_f))
    if status >= 0:
        Model_challenges.send_notification(nome, data_i, data_f)
        Model_challenges.insert_partecipazione(id_sfida=status)

    return redirect('/welcome?error='+str(status))

