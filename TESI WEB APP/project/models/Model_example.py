import mysql.connector, json
"""
    Import local package
from project.config.Database import connection as con, cursor as cur
from project.config.DatetimeEncoder import DatetimeEncoder
from project.config.Hash import Hash
"""
"""
    Your Code
"""


from project.models.classes.Prova import Prova
from .Model_interface import Model_interface # importo il modulo dalla stessa directory, è equivalente a quello sopra


class Model_example(Model_interface):
    '''implement model interface each method return an object of the relative class'''
    def __init__(self):
        pass

    def get_prova():
        return Prova()