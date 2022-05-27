from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime

"""
    Import local package
from project.config.Database import connection as con, cursor as cur
from project.config.DatetimeEncoder import DatetimeEncoder
from project.config.Hash import Hash
"""
"""
    Your Code
"""


from project.models.classes.User import User
from .Model_firstPage_interface import Model_firstPage_interface # importo il modulo dalla stessa directory, è equivalente a quello sopra


class Model_first_page(Model_firstPage_interface):
    '''implement model interface each method return an object of the relative class'''
    def __init__(self):
        pass

    def insert_new_user(email, nickname, image):

        query = 'SELECT * FROM utente WHERE nickname = \"' + nickname + '\"'

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            count = cur.rowcount
        
        state = 0    
        if count <= 0:
            query = 'INSERT INTO `utente`(`email`, `nickname`, `data_iscrizione`, `image`) VALUES (\"' + email +'\",\"' + nickname +'\",\"' + datetime.today().strftime('%Y-%m-%d') +'\",\"' + image +'\" )'

            with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
                cur = con.cursor(buffered=True)
                cur.execute(query)
                con.commit() #commit the changes -> use when you do an insert query
                state = cur.rowcount
            return state
        else: 
            print('record già presente')
            return False

        


    def get_user_nickname(email):
        #query = 'SELECT nickname FROM utente WHERE email = \"' + email + '\"'
        user = User(email)
        #with con:
        #    cur.execute(query)

        return user.get_nickname

    def is_registered(nickname):
        query = 'SELECT * FROM utente WHERE nickname = \"' + nickname + '\"'
        count = 0
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            count = cur.rowcount
        return count