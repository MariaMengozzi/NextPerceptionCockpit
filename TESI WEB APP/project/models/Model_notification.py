from project.config.Database import host, user, password, database, port
import mysql.connector
from datetime import datetime
from .Model_notification_interface import Model_notification_interface


class Model_notification(Model_notification_interface):
    def __init__(self):
        pass

    def insert_new_notification(text, nickname):
        query = 'INSERT INTO `notifica`(`data`, `testo`, `stato`, `nickname`) VALUES (\'%s\', \'%s\', 0, \'%s\')' %(datetime.today().strftime('%Y-%m-%d'), text, nickname)

        state = 0

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            con.commit()

            state = cur.rowcount
        return state

    def update_notification(id_notifica):
        query = 'UPDATE `notifica` SET `stato`=1 WHERE id_notifica=%d' %(id_notifica)

        state = 0

        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)
            con.commit()

            state = cur.rowcount
        return state

    def get_user_notifications(nickname):
        notification_list = []
        query = 'SELECT * FROM notifica WHERE nickname = \'%s\' and stato = 0' %(nickname)
        with mysql.connector.connect(host=host, user=user, password=password, database=database, port=port) as con :
            cur = con.cursor(buffered=True)
            cur.execute(query)

            rv = cur.fetchall()
            for result in rv:
                notification_list.append([*result]) #[*result] -> mappo da tupla a lista
            for i in range(len(notification_list)):
                notification_list[i][1] = notification_list[i][1].strftime('%Y-%m-%d')

        return notification_list