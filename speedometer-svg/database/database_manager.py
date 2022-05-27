import mysql.connector
import json
from decimal import Decimal

class Database(object):

    def __init__(self):
        print("Database create")

    
    def get_cockpit_data(self):
        query = 'SELECT * FROM `data` WHERE id = (SELECT MAX(id) FROM data)'
        json_data = {"id": 1, "torque": 0, "trasmissionGear": "first", "engineSpeed": 0, "vehicleSpeed": 0, "fuelConsumed": 0, "odometer": 0, "fuelLevel": 100, "heading": 0, "latitude": 42.3211, "longitude": -83.2373}

        with mysql.connector.connect(host="localhost", user="root", password="", database="obdsimulator", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            rv = db_cursor.fetchall()
            
            for result in rv:
                json_data = (dict(zip(row_headers,result)))

        return json.dumps(json_data)

    def get_elementOfDistraction_data(self):
        query = 'SELECT name, distractionelementvalues.value, colors.rgbColor FROM `distractionelement` JOIN colors ON color = colors.id JOIN distractionelementvalues ON distractionelement.id = distractionelementvalues.element WHERE distractionelementvalues.date = (SELECT MAX(date) FROM distractionelementvalues)' #(SELECT MAX(date) FROM distractionelementvalues) da sostituire con la data odierna (?)


        with mysql.connector.connect(host="localhost", user="root", password="", database="obdsimulator", port=3308) as db_connect :
            db_cursor = db_connect.cursor()
            db_cursor.execute(query)

            row_headers=[x[0] for x in db_cursor.description] #this will extract row headers
            rv = db_cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

        return json.dumps(json_data)
            
