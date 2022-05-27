from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime
import json


from .Model_profile_interface import Model_profile_interface # importo il modulo dalla stessa directory, è equivalente a quello sopra


class Model_profile(Model_profile_interface):
    '''implement model interface each method return an object of the relative class'''
    def __init__(self):
        pass

    def get_friends(nickname):
        query = 'SELECT nickname_seguito, nickname FROM seguaci WHERE nickname = \"' + nickname + '\" OR nickname_seguito = \"' + nickname + '\"'
        friends=[]
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            #row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()
            for result in rv:
                for r in result:
                    if r != nickname:
                        friends.append(r)

        return friends
    
    def are_friends(nick, nick_seguito):
        friend = 0
        query = 'SELECT * FROM `seguaci` WHERE nickname = \"' + nick + '\" AND nickname_seguito = \"' + nick_seguito + '\" OR nickname_seguito = \"' + nick + '\" AND nickname = \"' + nick_seguito + '\"'
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            friend = cur.rowcount

        return friend


    def insert_follower(nick, nick_seguito):
        state = 0
        query = 'INSERT INTO `seguaci` (`nickname`, `nickname_seguito`) VALUES ( \"' + nick + '\" , \"' + nick_seguito + '\")'
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            con.commit() #commit the changes -> use when you do an insert query
            state = cur.rowcount

        return state
    
    def get_profile_image(nickname):
        img = ''
        query = 'SELECT image FROM `utente` WHERE nickname = \"' + nickname + '\"'
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            img = cur.fetchone()[0]

        return img
    
    def get_personal_activities(nick):
        activities = []
        query = '''SELECT attivita.id_attivita, `data`, AVG(ftd_totale) as ftd FROM `ftd_attivita`
                JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita
                WHERE nickname = \'%s\' 
                GROUP BY attivita.id_attivita
                ORDER BY `data` DESC''' %nick
        
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            for result in rv:
                activities.append(dict(zip(row_headers,result)))

        return activities

    def get_element_and_ftd_group_by_days(nickname, day):
        elements_and_ftds = []
        today = datetime.today().strftime('%Y-%m-%d')
        query = '''SELECT AVG(`distrazione_visuale_tot`) AS DV, AVG(`distrazione_cognitiva_tot`) AS DC, AVG(`emozione_tot`) AS emotion,  AVG(`ftd_totale`) AS ftd, `timestamp` AS giorno FROM `ftd_attivita` 
            JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita
            WHERE nickname = \'%s\'
            GROUP BY `timestamp`
            ORDER BY `timestamp`
        ''' %nickname if not day else '''SELECT AVG(`distrazione_visuale_tot`) AS DV, AVG(`distrazione_cognitiva_tot`) AS DC, AVG(`emozione_tot`) AS emotion,  AVG(`ftd_totale`) AS ftd, `timestamp` AS giorno FROM `ftd_attivita` 
            JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita
            WHERE nickname = \'%s\'
            AND `timestamp` BETWEEN ( SELECT DATE_ADD(\'%s\', INTERVAL -10 DAY)) AND \'%s\' 
            GROUP BY `timestamp`
            ORDER BY `timestamp`
        ''' %(nickname, today, today)

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            for result in rv:
                elements_and_ftds.append(dict(zip(row_headers,result)))
            
            for i in range(len(elements_and_ftds)):
                elements_and_ftds[i]['giorno'] = elements_and_ftds[i]['giorno'].strftime('%Y-%m-%d')

        return json.dumps(elements_and_ftds)

    def get_element_and_ftd(nickname):
        elements_and_ftds = []
        query = '''SELECT AVG(`distrazione_visuale_tot`) AS DV, AVG(`distrazione_cognitiva_tot`) AS DC, AVG(`emozione_tot`) AS emotion,  AVG(`ftd_totale`) AS ftd FROM `ftd_attivita` 
            JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita
            WHERE nickname = \'%s\'
            ''' %nickname

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            for result in rv:
                elements_and_ftds.append(dict(zip(row_headers,result)))

        return json.dumps(elements_and_ftds)