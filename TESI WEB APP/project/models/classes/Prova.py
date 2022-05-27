from project.config.Database import host, user, password, database, port
import mysql.connector
class Prova():
    '''Prova class --> corespond to an handler class'''
    def __init__(self):
        self.text = "io sono la classe Prova" #attr text of Prova class
    
    def get_row(self):
        query = 'select * from colors'
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            for id, rgbColor in cur.fetchall():
                print(id, rgbColor)
            con.commit() #commit the changes -> use when you do an insert query
        return 'ok'
        