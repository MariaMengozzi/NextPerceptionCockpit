import mysql.connector
import json
from decimal import Decimal

from datetime import datetime

class Database(object):

    def __init__(self):
        print("Database create")
    '''  query = "SELECT * FROM premio"
        self.results = []
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            rv = db_cursor.fetchall()
            for result in rv:
                self.results.append(result[1])
                #json_data.append(dict(zip(row_headers,result)))

        
        '''

    def is_user_in_db(self, email):
        query = "SELECT * FROM utente WHERE nickname =\'%s\'" %email.replace('@gmail.com', '')
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3306) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)
            rv = db_cursor.fetchall()
            state = db_cursor.rowcount
        return state 

    def get_elementOfDistraction_data(self):
        #query = 'SELECT name, distractionelementvalues.value, colors.rgbColor FROM `distractionelement` JOIN colors ON color = colors.id JOIN distractionelementvalues ON distractionelement.id = distractionelementvalues.element WHERE distractionelementvalues.date = (SELECT MAX(date) FROM distractionelementvalues)' #(SELECT MAX(date) FROM distractionelementvalues) da sostituire con la data odierna (?)

        query = "SELECT AVG(distrazione_visuale_tot) as DV, AVG(distrazione_cognitiva_tot) as DC, AVG(emozione_tot) as Emozione from ftd_attivita WHERE id_auto = 0 AND `timestamp` = \'" + datetime.today().strftime('%Y-%m-%d')+"'"
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

    def get_last_10_FTD(self):
        today = datetime.today().strftime('%Y-%m-%d')
        query = "SELECT `timestamp` as giorno, AVG(ftd_totale) AS val FROM ftd_attivita WHERE id_auto = 0 AND `timestamp` BETWEEN ( SELECT DATE_ADD(\'"+ today +"\', INTERVAL -10 DAY)) AND \'"+ today+"\' GROUP BY `timestamp`"
        #timestamp contiene il res di datetime.datetime.now() --> 2020-07-15 14:30:26.159446 quindi lo faccio che contenga il giorno odierno

        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            rv = db_cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

            for i in range(len(json_data)):
                json_data[i]['giorno'] = json_data[i]['giorno'].strftime('%Y-%m-%d')

        return  json.dumps(json_data)         

    def insert_ftd_attivita(self, velocita, distrazione_visuale, distrazione_cognitiva, rabbia, felicita, paura, tristezza, disgusto, sorpresa, neutro, distrazione_visuale_tot, distrazione_cognitiva_tot, emozione_tot, ftd, id_auto, id_attivita):
        data = datetime.today().strftime('%Y-%m-%d')
        query = ''
        if id_attivita == 'Null':
            param = (velocita, distrazione_visuale, distrazione_cognitiva, rabbia, felicita, paura, tristezza, disgusto, sorpresa, neutro, distrazione_visuale_tot, distrazione_cognitiva_tot, emozione_tot, ftd, data, id_auto)
            query = 'INSERT INTO `ftd_attivita`(`velocita`, `distrazione_visuale`, `distrazione_cognitiva`, `rabbia`, `felicita`, `paura`, `tristezza`, `disgusto`, `sorpresa`, `neutro`, `distrazione_visuale_tot`, `distrazione_cognitiva_tot`, `emozione_tot`, `ftd_totale`, `timestamp`, `id_auto`) VALUES (%d, %.5f, %s, %s, %f, %f, %f, %f, %f, %f, %.6f, %.6f, %.6f, %f, \'%s\', %d)' % param
        else:
            param = (velocita, distrazione_visuale, distrazione_cognitiva, rabbia, felicita, paura, tristezza, disgusto, sorpresa, neutro, distrazione_visuale_tot, distrazione_cognitiva_tot, emozione_tot, ftd, data , id_auto,id_attivita)
            query = 'INSERT INTO `ftd_attivita`(`velocita`, `distrazione_visuale`, `distrazione_cognitiva`, `rabbia`, `felicita`, `paura`, `tristezza`, `disgusto`, `sorpresa`, `neutro`, `distrazione_visuale_tot`, `distrazione_cognitiva_tot`, `emozione_tot`, `ftd_totale`, `timestamp`, `id_auto`, `id_attivita`) VALUES (%d, %.5f, %s, %s, %f, %f, %f, %f, %f, %f, %.6f, %.6f, %.6f, %f, \'%s\', %d, %d)' % param
        print(query)


        state = 0
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            con.commit() #commit the changes -> use when you do an insert query
            state = cur.rowcount

        return state

    def get_id_attivita(self, email):
        nick = email.replace('@gmail.com', '')
        # seleziono max id_attività da attività dove nickname = nick e la data è <= di quella odierna.
        # se non è presente allora faccio una nuova insert e ritorno l'id della nuova attività
        param = (nick, str(datetime.today().strftime('%Y-%m-%d')))
        query = 'SELECT id_attivita as id FROM `attivita` WHERE nickname = \"%s\" and `data` = \"%s\" ' %param
        #print(query)
        id = -1
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            result = cur.fetchone()
            state = cur.rowcount
            if cur.rowcount == 1 and result[0] is not None:
                id = result[0]
            else:
                id = self.insert_attivita(nick)
        #print(id)
        return  id 

    def insert_attivita(self,nickname):
        query = 'INSERT INTO `attivita`(`data`, `nickname`) VALUES (\"%s\",\"%s\")' %(str(datetime.today().strftime('%Y-%m-%d')), nickname)
        id = -1
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            id = cur.lastrowid
        return id

    def manage_activity_results(self, id_attivita, email):
        #check if id activity is in results table: if true update resuls if are change, if id activity doesn't exist inser new result
        query = 'SELECT id_attivita as id_a FROM `risultati` WHERE id_attivita = %d' %int(id_attivita)
        #print(query)
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            result = cur.fetchone()
            #state = cur.rowcount
            if cur.rowcount >= 1 and result[0] is not None:
                self.delete_old_result(id_attivita)
            
            resG = self.get_result_global(id_attivita)
            if resG != -1 :
                self.insert_result(id_attivita, resG)
            nickname = email.replace('@gmail.com', '')
            resP = self.get_personal_result(id_attivita, nickname)
            if resP != -1 :
                self.insert_result(id_attivita, resP)
    
    def get_result_global(self, id_activity):
        query ='SELECT attivita.id_attivita, AVG(ftd_totale) as ftd FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita WHERE attivita.id_attivita = %d GROUP BY attivita.id_attivita' %id_activity
        print(query)
        res = -1
        ftd = None
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            for r in results:
                ftd = r[1]


        query = 'SELECT attivita.id_attivita, AVG(ftd_totale) as ftd FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita GROUP BY attivita.nickname ORDER BY AVG(ftd_totale) DESC LIMIT 10'
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            
            for i, result in enumerate(results):
                if ftd >= result[1]:
                    res = i
        return res

    def get_personal_result(self, id_activity, nickname):
        query ='SELECT attivita.id_attivita, AVG(ftd_totale) as ftd FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita WHERE attivita.id_attivita = %d GROUP BY attivita.id_attivita' %id_activity
        res = -1
        ftd = None
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            for r in results:
                ftd = r[1]


        query = 'SELECT attivita.id_attivita, AVG(ftd_totale) as ftd FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita WHERE nickname = \'%s\' GROUP BY attivita.id_attivita ORDER BY AVG(ftd_totale) DESC LIMIT 3' %nickname
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            
            for i, result in enumerate(results):
                if ftd >= result[1]:
                    res = i + 12 # perchè le prime 10 sono per la classifica globale e l'11 non c'è 
        return res

    def insert_result(self, id_a, res):
        if res != 10:
            query = 'UPDATE `risultati` SET `id_premio`=`id_premio`+1 WHERE id_premio BETWEEN %d and 10' %(res)
            id = -1
            with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
                cur = con.cursor()
                cur.execute(query)
                con.commit()
                id = cur.lastrowid

            query = 'INSERT INTO `risultati`(`id_premio`, `id_attivita`) VALUES (%d, %d)' %(res, id_a)
            id = -1
            with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
                cur = con.cursor()
                cur.execute(query)
                con.commit()
                id = cur.lastrowid
            return id
        
    def delete_old_result(self, id_activity):
        query = 'DELETE FROM `risultati` WHERE id_attivita = %d' %id_activity
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            con.commit()
    

        

            