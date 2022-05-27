from random import random
from project import app
from flask import render_template, redirect, url_for, request, session
import random

# decorator for routes that should be accessible only by logged in users
from project.models.auth_decorator import login_required



from project.models.Model_welcome import Model_welcome
from project.models.Model_notification import Model_notification
from project.models.Model_challenges import Model_challenges

#route index

''' tips = [
    'Hai mai notato che chiunque vada più lento di te è un idiota, ma chiunque vada più veloce è un pazzo?',
    'Non guidare nel caso in cui si abbia sonno, subito dopo un pasto molto abbondante o nel caso di uso di farmaci che inducano sonnolenza.'
    'In caso di fondo stradale viscido per pioggia, ghiaccio o altre sostanze, mantenere sempre una velocità moderata ed utilizzare i comandi dell’auto, soprattutto volante e freni, in modo graduale, evitando manovre o azioni brusche.',
    'L’alcol è un nemico per tutti gli utenti della strada. Chi guida in stato di ebbrezza, mette a rischio la propria vita e quella dei malcapitati che incontra durante il suo tragitto. Se si guida non si deve bere. ',
    'non usare il telefono, causa primaria di incidenti su strada. L’utilizzo dello smartphone è severamente vietato dal Codice della Strada durante la guida, si rischiano infatti gravi sanzioni. Non è obbligatorio spegnerlo, ma bisogna usare il sistema Bluetooth della macchina o gli auricolari, per parlare senza avere in mano lo smartphone;',
    'masticare una gomma può aiutare a evitare distrazioni e disattenzioni proveniente da stimoli esterni. Spezza infatti la monotonia di un viaggio lungo, la noia nel traffico;',
    'ascoltare la musica può aiutare a non distrarsi, se si vuole evitare un colpo di sonno, tenerla ad alto volume può essere la soluzione (raccomandiamo di fermarsi sempre e riposare quando ci si sente stanchi mentre si è al volante, continuare a guidare potrebbe essere estremamente pericoloso);',
    'chiacchierare con altri passeggeri in auto può aiutare a evitare di distrarsi o addormentarsi mentre si è alla guida della macchina. Evitate però discussioni o toni particolarmente accesi, perché chiaramente distolgono l’attenzione da quello che state facendo; eventualmente fermatevi e chiarite la situazione prima di ripartire, fate lo stesso se i bimbi in auto fanno troppa confusione;',
    'controllate che i bambini siano ben agganciati ai loro seggiolini, in modo che non possano intralciarvi durante la guida e nemmeno rischiare la loro salute in caso di brusche frenate;',
    'può essere molto utile anche prendere aria, soprattutto quando fa caldo, abbassare il finestrino per far entrare un po’ di fresco può aiutare a non distrarsi e anzi a dare una scossa piacevole al viaggio.'
] '''



@app.route('/welcome', methods = ['GET','POST'])
@login_required
def welcome():
    '''print(dict(session).get('email', None))
    if dict(session).get('email', None) == None:
        return redirect('/')
    else:'''
    if dict(session).get('nickname', None) == 'aftd26524': #email dell'aministratore
        error = False
        if request.args.get('error') is not None:
            error = True if request.args.get('error') == '-1' else False
        data = {
        "title": "Admin home",
        "name": "admin_home.html",
        'error': error,
        'challenges': Model_challenges.get_all_challenges()
        }
        return render_template('admin_base.html', data = data)
    else :
        m = Model_welcome(app)
        tip = m.get_random_tip()
        text = "welcome to the application" if dict(session).get('new_user', None) else tip#tips[random.randint(0, len(tips))]
        if dict(session).get('new_user', None):
            notification_text = 'Benvenuto ' +str(dict(session).get('nickname', None)).upper()+', adesso fai parte della community anche te!'
            
            if Model_notification.insert_new_notification(notification_text, dict(session).get('nickname', None)):
                print('inserimento notifica OK')
            else:
                print('errore inserimento notifica')

        data = {
            "title": "Welcome",
            "name": "welcome_page.html",
            "first": True,
            "text" : text,
            "new" : dict(session).get('new_user', None)
        }
        session.pop('new_user', None)    

        return render_template('base.html', data = data)