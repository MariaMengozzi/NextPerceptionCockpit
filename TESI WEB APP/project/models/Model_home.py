from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime
import json


from .Model_home_interface import Model_home_interface # importo il modulo dalla stessa directory, è equivalente a quello sopra


class Model_home(Model_home_interface):
    def __init__(self):
        pass

    def get_activities(nick):
        activities = []
        query = '''SELECT attivita.id_attivita, `data`, AVG(ftd_totale) as ftd, nickname FROM `ftd_attivita`
                JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita
                WHERE  nickname IN (SELECT DISTINCT nickname FROM seguaci WHERE nickname_seguito = \'%s\') 
                OR nickname IN (SELECT DISTINCT nickname_seguito FROM seguaci WHERE nickname = \'%s\') 
                OR nickname = \'%s\'
                GROUP BY attivita.id_attivita
                ORDER BY `data` DESC''' %(nick,nick, nick)
        
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            for result in rv:
                activities.append(dict(zip(row_headers,result)))

        return activities

    def get_profile_image_from_nick(nick):
        img = ''
        query = 'SELECT image FROM `utente` WHERE nickname = \"' + nick + '\"'
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            img = cur.fetchone()[0]

        return img