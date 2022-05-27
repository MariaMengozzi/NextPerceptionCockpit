from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime
from .Model_activity_interface import Model_activity_interface
from .Model_notification import Model_notification
import json

class Model_activity(Model_activity_interface):
    def __init__(self):
        pass

    def get_likes_number(id_attivita):
        likes = 0
        query = 'SELECT COUNT(id_attivita) FROM likes WHERE id_attivita = %d' %id_attivita
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            likes = cur.fetchone()[0]

        return likes 
    
    def set_like(id_attivita, nickname):
        status = 0
        query = 'INSERT INTO `likes`(`id_attivita`, `nickname`) VALUES (%d,\'%s\')' %(id_attivita, nickname)
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            status = cur.rowcount
            con.commit()

        if status == 1:
            info = []
            query = 'SELECT data, utente.nickname FROM utente JOIN attivita ON utente.nickname = attivita.nickname WHERE id_attivita = %d ' %id_attivita
            with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
                cur = con.cursor(buffered=True)
                cur.execute(query)
                #row_headers=[x[0] for x in cur.description] #this will extract row headers
                info = cur.fetchone()

            text = nickname + ' ha messo il like alla tua attività del ' + info[0].strftime('%Y-%m-%d')
            status = Model_notification.insert_new_notification(text, info[1])

        return status

    def has_like(id_activity, nickname):
        has_like = 0
        query = 'SELECT * FROM likes WHERE id_attivita = %d AND nickname = \'%s\'' %(id_activity, nickname)
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            has_like = cur.rowcount

        return 0 if has_like <= 0 else has_like

    def get_image_from_activity(id_activity):
        img = 0
        query = 'SELECT image FROM utente JOIN attivita ON utente.nickname = attivita.nickname WHERE id_attivita = %d ' %id_activity
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            img = cur.fetchone()[0]

        return img 

    def get_info_from_id(id_activity):
        info = []
        query = 'SELECT data, utente.nickname FROM utente JOIN attivita ON utente.nickname = attivita.nickname WHERE id_attivita = %d ' %id_activity
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            for result in rv:
                info.append(dict(zip(row_headers,result)))

        return info

    def get_results_activity(id_activity):
        query = 'SELECT `nome` FROM `premio` JOIN `risultati` ON premio.id_premio = risultati.id_premio WHERE id_attivita= %d' %id_activity
        premi = []
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            rv = cur.fetchall()
            for result in rv:
                premi.append(result[0])

        return premi

    def get_elementOfDistraction_data(id_activity):
        query = "SELECT AVG(distrazione_visuale_tot) as DV, AVG(distrazione_cognitiva_tot) as DC, AVG(emozione_tot) as Emozione from ftd_attivita WHERE id_attivita = %d" %id_activity
        #timestamp contiene il res di datetime.datetime.now() --> 2020-07-15 14:30:26.159446 quindi lo faccio che contenga il giorno odierno

        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            #row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            row_headers = ['DV', 'DC', 'emotion']
            rv = db_cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

        return json.dumps(json_data)

    def get_FTD_single_activity(id_activity):
        query = "SELECT  ftd_totale AS val FROM ftd_attivita WHERE id_attivita = %d " %id_activity#LIMITARLO a N res(?) 

        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            rv = db_cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

        return  json.dumps(json_data)         


