from numpy import TooHardError
from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime
from .Model_challenges_interface import Model_challenges_interface
import os
from werkzeug.utils import secure_filename
from pathlib import Path  
from .Model_notification import Model_notification 
from datetime import datetime



class Model_challenges(Model_challenges_interface):
    def __init__(self):
        pass

    def insert_new_challenge(nome, badge, data_i, data_f):
        id = -1
        
        query = "INSERT INTO `sfida`(`nome`, `badge`, `data_inizio`, `data_fine`) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')" %(nome,badge, data_i, data_f)

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            con.commit()

            id = cur.lastrowid
        return id 


    def get_all_challenges():
        challeges = []
        query = 'SELECT id_sfida, nome, data_inizio, data_fine, badge  FROM `sfida` ORDER BY `data_inizio` DESC' 
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            rv = cur.fetchall()
            for result in rv:
                d1 = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                gg_trascorsi = (d1 - d2).days if (d1 - d2).days >0 else 0
                d1 = datetime.strptime(result[3].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                gg_sfida = (d1 - d2).days if (d1 - d2).days >0 else 0

                avanzamento = round((gg_trascorsi / gg_sfida) * 100) if gg_trascorsi < gg_sfida else 100
                challenge = [result[0], result[1], avanzamento, result[4]] #correggi
                #challenge = [result['nome'], 100 - 100 * result['giorni_rimanenti'] / result['giorni_tot'], result['badge']]
                challeges.append(challenge)

        return challeges

    def save_image(img):
        filename = secure_filename(img.filename)
        path =  os.path.join(os.path.abspath(os.path.dirname(__file__)) + '/../static/image/challenge_badges', filename.replace(' ', '')).replace ('\\', '/')
        img.save(path)
        return Path(path).name

    def send_notification(nome, data_i, data_f):
        users = []
        msg = '''É stata inserita una nuova sfida:<br>Nome sfida: %s <br>Data inizio: %s <br>Data fine: %s <br>Fai del tuo meglio per essere tra i migliori !''' %(nome, data_i, data_f)

        query = 'SELECT nickname FROM `utente` WHERE nickname != "aftd26524"'  #aftd26524 -> nickname admin
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            rv = cur.fetchall()
            for result in rv:
                users.append(result[0])

        for u in users:
            Model_notification.insert_new_notification(msg, u)
    
    def get_filtered_challenges():
        finished_c= []
        ongoing_c = []
        query = 'SELECT id_sfida, nome, data_inizio, data_fine, badge  FROM `sfida` ORDER BY `data_inizio` DESC' 
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            rv = cur.fetchall()
            for result in rv:
                d1 = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                gg_trascorsi = (d1 - d2).days if (d1 - d2).days >0 else 0
                d1 = datetime.strptime(result[3].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
                gg_sfida = (d1 - d2).days if (d1 - d2).days >0 else 0

                avanzamento = round((gg_trascorsi / gg_sfida) * 100) if gg_trascorsi < gg_sfida else 100
                challenge = [result[0], result[1], avanzamento, result[4]] #correggi
                #challenge = [result['nome'], 100 - 100 * result['giorni_rimanenti'] / result['giorni_tot'], result['badge']]
                if avanzamento <100:
                    ongoing_c.append(challenge)
                else:
                    finished_c.append(challenge)

        return ongoing_c , finished_c

    def insert_partecipazione(id_sfida):
        users=[]
        query = 'SELECT nickname FROM `utente` WHERE nickname != "aftd26524"'  #aftd26524 -> nickname admin
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            rv = cur.fetchall()
            for result in rv:
                users.append(result[0])

        for u in users:
            query = 'INSERT INTO `partecipazione_sfida`(`id_sfida`, `nickname`) VALUES (%d,\'%s\')' %(id_sfida, u)
            with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
                cur = con.cursor(buffered=True)
                cur.execute(query)
                con.commit()
    
    def get_ranking_challenge(id_challenge):
        query = 'SELECT `data_inizio`, `data_fine` FROM `sfida` WHERE id_sfida = %d' %id_challenge

        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchone()
            di = results[0].strftime('%Y-%m-%d')
            df = results[1].strftime('%Y-%m-%d')


        query = 'SELECT image, attivita.nickname FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita JOIN utente ON utente.nickname = attivita.nickname WHERE timestamp BETWEEN \'%s\' AND \'%s\' GROUP BY attivita.nickname ORDER BY AVG(ftd_totale) DESC LIMIT 10' %(di,df)
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            res = []
            for r in results:
                res.append(r)
        return res

    def get_challenge_info(id_challenge):
        query = 'SELECT id_sfida, nome, data_inizio, data_fine, badge FROM `sfida` WHERE id_sfida = %d' %id_challenge

        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            result = cur.fetchone()

            d1 = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            gg_trascorsi = (d1 - d2).days if (d1 - d2).days >0 else 0
            d1 = datetime.strptime(result[3].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            d2 = datetime.strptime(result[2].strftime("%Y-%m-%d"), "%Y-%m-%d").date()
            gg_sfida = (d1 - d2).days if (d1 - d2).days >0 else 0

            avanzamento = round((gg_trascorsi / gg_sfida) * 100) if gg_trascorsi < gg_sfida else 100
            return [result[1], avanzamento, result[4]]
