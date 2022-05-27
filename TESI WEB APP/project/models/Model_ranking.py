from project.config.Database import host, user, password, database, port
import mysql.connector

from .Model_ranking_interface import Model_ranking_interface

class Model_ranking(Model_ranking_interface):
    def __init__(self):
        pass

    def get_ranking():
        query = 'SELECT  image, attivita.nickname,AVG(ftd_totale) as ftd FROM `ftd_attivita` JOIN attivita ON attivita.id_attivita = ftd_attivita.id_attivita JOIN utente ON utente.nickname = attivita.nickname GROUP BY attivita.nickname ORDER BY AVG(ftd_totale) DESC LIMIT 10'
        with mysql.connector.connect(host="localhost", user="root", password="", database="progetto_tesi", port=3308) as con :
            cur = con.cursor()
            cur.execute(query)
            results = cur.fetchall()
            res = []
            for r in results:
                res.append(r)
        return res
        