from types import DynamicClassAttribute
from flask import Flask, jsonify, render_template, request, session, url_for, redirect
#from database.database_manager import Database -> install mysql and mysql client
from authlib.integrations.flask_client import OAuth

import paho.mqtt.client as mqtt
from threading import Thread
import threading

import random
import json

import numpy as np
import pandas as pd
import datetime
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '8f42a73054b1749f8f58848be5e6502c'  # da cambiare

# thread and mqtt config
lock = threading.Lock()
sessionId = 0

class BrokerNameException(Exception):
    """Raised when the broker name is none or empty """
    def __init__(self, message="the broker name is none or empty"):
        self.message = message
        super().__init__(self.message)

class PortNumberException(Exception):
    """Raised when the port number is none"""
    def __init__(self, message="the port number is none"):
        self.message = message
        super().__init__(self.message)

class EmptyMessageException(Exception):
    """Raised when the message is empty"""
    def __init__(self, topic, message="the message is empty"):
        self.topic = topic
        self.message = self.topic +': '+ message
        super().__init__(self.message)


FTD_MAX_PUBLISH = 1

FTD = 1

IDC = 0
IDV = 0
threshold_i_c = 1
threshold_i_v = 2
weight = 1.01
threshold_v = 300
decimals = 4
weight_anger = 0.125
weight_happiness = 0.125
weight_fear = 0.083
weight_sadness = 0.083
weight_neutral = 0
weight_disgust = 0.042
weight_sorprise = 0.042
weights_emozioni = pd.Series([weight_anger, weight_happiness, weight_fear, weight_sadness, weight_neutral, weight_disgust, weight_sorprise])
s = 0 #speed value
Ei = 0
DCi = 0
DVi = 0
timestamp_relab=0
arousal=0

flagE = False
flagD = False
flagV = False



#variable for log
anger = 0
happiness = 0
fear = 0
sadness = 0
neutral = 0
disgust = 0
surprise = 0
cd = 0 #cognitive distraction value
vd = 0 #visual distraction value

anger_buffer = [0,0,0,0]
happiness_buffer = [0,0,0,0]
fear_buffer = [0,0,0,0]
sadness_buffer = [0,0,0,0]
neutral_buffer = [0,0,0,0]
disgust_buffer = [0,0,0,0]
surprise_buffer = [0,0,0,0]
speed_buffer = [0,0,0,0]
arousal_buffer = [0, 0, 0, 0]  # 1 arousal max, 0 arousal min


user = 'person0'

# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code {0}".format(str(rc)))
    #client.subscribe("mytopic")
    client.subscribe('NP_UNITO_DCDC', qos=1)
    client.subscribe('Emotions', qos=1)
    client.subscribe('AITEK_EVENTS', qos=1)
    client.subscribe('NP_RELAB_VD', qos=1)# Effective speed
    client.subscribe('NP_UNIBO_FTD', qos=1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global FTD, IDC, IDV, weight, decimals, threshold_v, threshold_i_v, threshold_i_c, DCi, DVi, s, Ei, flagD, flagE, flagV
    global anger, happiness, fear, sadness, neutral, disgust, surprise, cd, vd, arousal 
    global anger_buffer, happiness_buffer, fear_buffer, sadness_buffer, neutral_buffer, disgust_buffer, surprise_buffer, speed_buffer, timestamp_relab, arousal_buffer
    global user
    #print("topic: "+msg.topic)

    if msg.topic == 'NP_RELAB_VD':
        try:
            if len(str(msg.payload.decode('utf-8'))) == 0:
                raise EmptyMessageException(topic='NP_RELAB_VD')
            else:
                s = json.loads(str(msg.payload.decode("utf-8")))
                timestamp_relab = s['VehicleDynamics']['timestamp']
                speed_buffer.pop(0)
                speed_buffer.append(s['VehicleDynamics']['speed']['x'])

        except Exception as exception:
            print(exception)
        

        #flagV = True
    elif msg.topic == 'NP_UNITO_DCDC':
        try:
            if len(str(msg.payload.decode('utf-8'))) == 0:
                raise EmptyMessageException(topic='NP_UNITO_DCDC')
            else:
                D = json.loads(str(msg.payload.decode("utf-8")))

                cd = D['cognitive_distraction'] if D['cognitive_distraction_confidence'] != 0 else 0.0
                if D['cognitive_distraction_confidence'] == 0.0:
                    print('NO cognitive distraction value')

        except Exception as exception:
            cd = 0.0
            print(exception)


        speed_mean = np.mean(speed_buffer)
        if (cd):
            IDC +=1
        else:
            IDC = 0
        DCi = round(cd * speed_mean/threshold_v * weight **(IDC - threshold_i_c), decimals)

        flagD = True

    elif msg.topic == 'AITEK_EVENTS':
        try:
            if len(str(msg.payload.decode('utf-8'))) == 0:
                raise EmptyMessageException(topic='AITEK_EVENTS')
            else:
                D = json.loads(str(msg.payload.decode("utf-8")))
                vd = 1 if D['start'] == 'True' else 0

        except Exception as exception:
            vd = 0
            print(exception)

    elif msg.topic == 'Emotions':
        try:
            e = {}
            if len(str(msg.payload.decode('utf-8'))) == 0:
                e = {"predominant" : "0","neutral":"0","happiness": "0","surprise":"0","sadness": "0","anger": "0","disgust": "0","fear": "0","engagement": "0","valence": "0"}
                raise EmptyMessageException(topic='Emotions')

            if len(json.loads(str(msg.payload.decode("utf-8")))) == 0:
                e = {"predominant" : "0","neutral":"0","happiness": "0","surprise":"0","sadness": "0","anger": "0","disgust": "0","fear": "0","engagement": "0","valence": "0"}
                print('NO emotion value')
            else:
                e = json.loads(str(msg.payload.decode("utf-8")))[user]
        
            anger_buffer.pop(0)
            happiness_buffer.pop(0)
            fear_buffer.pop(0)
            sadness_buffer.pop(0)
            neutral_buffer.pop(0)
            disgust_buffer.pop(0)
            surprise_buffer.pop(0)

            anger_buffer.append(float(e['anger']))
            happiness_buffer.append(float(e['happiness']))
            fear_buffer.append(float(e['fear']))
            sadness_buffer.append(float(e['sadness']))
            neutral_buffer.append(float(e['neutral']))
            disgust_buffer.append(float(e['disgust']))
            surprise_buffer.append(float(e['surprise']))
        except Exception as exception:
                print(exception)
        #emotions_total= Ei

    elif msg.topic == 'NP_UNIPR_AROUSAL':

        try:
            data = json.loads(str(msg.payload.decode("utf-8")))
            print(data)
            if len(str(msg.payload.decode('utf-8'))) == 0:
                
                print('NO arousal value')
            elif "arousal" in data:
                arousal_buffer.pop(0)
                arousal_buffer.append(data['arousal'])
                arousal = np.mean(arousal_buffer)
        except Exception as exception:
                print(exception)

    elif msg.topic == 'NP_UNIBO_FTD':
        try:
            if len(str(msg.payload.decode('utf-8'))) == 0:
                raise EmptyMessageException(topic='NP_UNIBO_FTD')
            else:
                FTD = json.loads(str(msg.payload.decode("utf-8")))['person0']['ftd']
        except Exception as exception:
            print(exception)

    if flagD: #flagE and flagD and flagV:

        anger = np.mean(anger_buffer)
        happiness = np.mean(happiness_buffer)
        fear = np.mean(fear_buffer)
        sadness = np.mean(sadness_buffer)
        neutral = np.mean(neutral_buffer)
        disgust = np.mean(disgust_buffer)
        surprise = np.mean(surprise_buffer)

        emotions = pd.Series([anger, happiness, fear, sadness, neutral, disgust, surprise])
        
        Ei =  round(((emotions * weights_emozioni).sum() / weights_emozioni.sum()) * arousal, decimals)

        if (vd):
            IDV +=1
        else:
            IDV = 0 

        DVi = round(vd * speed_mean/threshold_v * weight **(IDV - threshold_i_v), decimals)

        ftd = {user:{
            'timestamp': timestamp_relab,
            'ftd' : max(0, 1 - (DCi + DVi + Ei))
            }}
        client.publish("NP_UNIBO_FTD", json.dumps(ftd))

        msg = {
            'FTD': max(0, 1 - (DCi + DVi + Ei)),
            'cognitive distraction' : cd,
            'visual distraction': vd,
            'emotion': {
                    'anger': anger,
                    'happiness': happiness,
                    'fear': fear,
                    'sadness': sadness,
                    'neutral': neutral,
                    'disgust': disgust,
                    'surprise': surprise
            },     
        'speed': np.mean(speed_buffer)
        }

        
        #flagE = False
        flagD = False
        #flagV = False
        #FTDs.append(max(0, 1 - (DCi + DVi + Ei)))

    


client = mqtt.Client(client_id="foo", clean_session=True)
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
#client.username_pw_set(mqtt_user, mqtt_password)
client.connect("broker.hivemq.com", port=1883)

client2 = mqtt.Client(client_id="foo", clean_session=True)
client2.on_connect = on_connect  # Define callback function for successful connection
client2.on_message = on_message  # Define callback function for receipt of a message
#client.username_pw_set(mqtt_user, mqtt_password)
client2.connect("broker.mqttdashboard.com", port=8000)
#client.loop_start()


def test(param1, param2):
    lock.acquire()
    client.loop_forever();
    #try:
    #    ret = client.publish("mytopic", "foo")
    #finally:
    lock.release()
    #    result = "foo"

    #return result


# oauth config

""" @app.route('/')
#@login_required --> https://github.com/Vuka951/tutorial-code/blob/master/flask-google-oauth2/ è in oauth decorator
def hello_world():
    #email = dict(session)['profile']['email']
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as {email}!' """


@app.route('/', methods=['GET'])
def home():
    global FTD, IDC, IDV, DCi, DVi, s, Ei, flagD, flagE, flagV
    global anger, happiness, fear, sadness, neutral, disgust, surprise, cd, vd, arousal 
    global arousal_buffer, anger_buffer, happiness_buffer, fear_buffer, sadness_buffer, neutral_buffer, disgust_buffer, surprise_buffer, speed_buffer, timestamp_relab

    FTD = 1
    IDC = 0
    IDV = 0

    s = 0 #speed value
    Ei = 0
    DCi = 0
    DVi = 0
    timestamp_relab=0
    arousal=0

    flagE = False
    flagD = False
    flagV = False

    anger_buffer = [0,0,0,0]
    happiness_buffer = [0,0,0,0]
    fear_buffer = [0,0,0,0]
    sadness_buffer = [0,0,0,0]
    neutral_buffer = [0,0,0,0]
    disgust_buffer = [0,0,0,0]
    surprise_buffer = [0,0,0,0]
    speed_buffer = [0,0,0,0]
    arousal_buffer = [0, 0, 0, 0]  # 1 arousal max, 0 arousal min

    for key in list(session.keys()):
        session.pop(key)
    return render_template("CarHome.html", data={'msg': 0 if request.args.get('msg') is None else 1})

# non è presente il login del'auto perchè sarà di default inserito al momento dell'installzione dell'applicazione nella macchina




@app.route('/cockpit')
def cockpit():
    # app.route('/cockpit')
    email = dict(session).get('email', None)
    print(email)
    t = Thread(target=test, args=(sessionId, None))
    t.start()
    return render_template("CarCockpit.html")


@app.route('/publish_data')
def publish_data():
    global s
    decimals = 4

    start = 0

    client.loop_start()
    #client.on_subscribe = on_subscribe
    #client.on_message = on_message

    anger = 0
    disgust = 0
    fear = 0
    joy = 0
    neutral = 0
    sadness = 0
    surprise = 0
    arousal = 0

    for k in range(4):
        speedVal = random.randint(0, 140)
        anger = round(random.random(),decimals) # num casuale tra 0 e 1
        disgust = round(random.uniform(0, 1-anger), decimals)
        fear = round(random.uniform(0, 1-(anger + disgust)), decimals)
        joy = round(random.uniform(0, 1-(anger + disgust + fear)), decimals)
        neutral = round(random.uniform(0, 1-(anger + disgust + fear + joy)), decimals)
        sadness = round(random.uniform(0, 1-(anger + disgust + fear + joy + neutral)), decimals)
        surprise = round(1 - (anger + disgust + fear + joy + neutral + sadness), decimals)

        emotion_topic = ['{"person0" : {"predominant" : "0","neutral":"'+ str(neutral)+'","happiness": "'+str(joy)+'","surprise":"'+str(surprise)+'","sadness": "'+str(sadness)+'","anger": "'+str(anger)+'","disgust": "'+str(disgust)+'","fear": "'+str(fear)+'","engagement": "4.4877","valence": "0.0154492"} }']
        emotion = random.choice(emotion_topic)
        speed = '{"VehicleDynamics": { "COGPos": { "x": 2674.6463496370525, "y": -14.564664744839954, "z": 0.45894402610593055 }, "GearBoxMode": 10, "acceleration": { "heading": -0.0033882581628859043, "pitch": 1.0706313332775608e-05, "roll": -0.0091178948059678078, "x": 0.28764855861663818, "y": 0.11754922568798065, "z": 0.0011688719969242811 }, "accelerator": 1, "brake": 0, "clutch": 0, "engineSpeed": 397.5355224609375, "engineStatus": 1, "gearEngaged": 6, "position": { "heading": -2.4471809390732866, "pitch": 0.0010818612183405301, "roll": 0.0064789495254821217, "x": 2675.8232267297335, "y": -13.584974385944776, "z": -0.0013803915935547695 }, "radarInfos": { "angle": 1110634.625, "anglesx": 0, "anglesy": 0, "anglesz": 0, "azimuth": 0, "distanceToCollision": 0, "id": 0, "laneId": 0, "posx": 0, "posy": 0, "posz": 0, "roadId": 0, "speed": 0, "visibility": 0 }, "roadInfo": { "intersectionId": -1, "laneGap": -0.049474708735942841, "laneId": 2, "roadAbscissa": 679.15997314453125,  "roadAngle": -3.141146183013916, "roadGap”": 1.7005252838134766, "roadId": 37 }, "speed": { "heading": 0.003960845060646534, "pitch": 6.9768051616847515e-05, "roll": 0.0023608640767633915,  "x": '+ str(speedVal) +', "y": -0.029801525175571442, "z": 0.054808627814054489 }, "steeringTorq": -0.052799351513385773, "steeringWheelAngle": 0.0067141000181436539, "steeringWheelSpeed": -0.016700951382517815,  "timestamp": 1631180995458, "wheelAngle": 0.00025969580747187138 }, "wheelState": { "0": { "angle": 1110634.625, "grip": 1,"laneType": 3, "posx": 2.6995155811309814, "posy": 0.75018519163131714, "posz": 0.3011646568775177, "rotx": 0.00028212839970365167, "roty": -0.060661893337965012, "rotz": 0.0025958430487662554, "speed": 161.23155212402344, "vhlDelta": -0.0030761519446969032, "vhlSx": 0.069431886076927185 }, "1": { "angle": 1109191, "grip": 1, "laneType": 3, "posx": 2.6995253562927246, "posy": -0.75022125244140625, "posz": 0.30186328291893005, "rotx": -0.00028936716262251139, "roty": -0.060574695467948914, "rotz": -0.0020764514338225126, "speed": 161.22161865234375, "vhlDelta": 0.0015965558122843504, "vhlSx": 0.0067795705981552601 }, "2": { "angle": 1099277.125, "grip": 1, "laneType": 3, "posx": -0.0020916683133691549, "posy": 0.74077975749969482, "posz": 0.30334118008613586, "rotx": 0.0019761791918426752, "roty": -0.13483227789402008, "rotz": -0.0015447111800312996, "speed": 160.06707763671875, "vhlDelta": 0.00085329683497548103, "vhlSx": -0.00049092137487605214 }, "3": { "angle": 1101188, "grip": 1, "laneType": 3, "posx": -0.002209091791883111, "posy": -0.74075996875762939, "posz": 0.30403971672058105, "rotx": -0.0021273412276059389, "roty": -0.13346090912818909, "rotz": 0.0015314865158870816, "speed": 160.07774353027344, "vhlDelta": -0.022224732674658298, "vhlSx": -0.00048526551108807325 } } }'

        s = speed

        arousal_topic = [
            json.dumps({"arousal": 0}),
            json.dumps({"arousal": round(random.random(), decimals)}),
            json.dumps({"arousal": 1})
        ]
        arousalSend = random.choice(arousal_topic)
        arousal = json.loads(arousalSend)["arousal"]

        client.publish('NP_UNIPR_AROUSAL',arousalSend)
        client.publish('Emotions', emotion)

        client2.publish('Emotions', emotion)
        
        client.publish('NP_RELAB_VD', speed)

    DC = random.randint(0, 1)
    eyesOffRoad = random.randint(0, 1)
    confidence_value =[0.0, round(random.random(),1)]
    DC_topic = ['{"time": 123456, "eyesOffRoad": ' +str(eyesOffRoad)+',"cognitive_distraction":'+str(DC)+', "eyesOffRoad_confidence": '+str(random.choice(confidence_value))+',  "cognitive_distraction_confidence": '+str(random.choice(confidence_value))+', "eyesOffRoad_pred_1s": 0.0, "cognitive_distraction_pred_1s": 0.0 }']
    D = random.choice(DC_topic)
    client.publish('NP_UNITO_DCDC', D)
    
    DV = random.randint(0, 1)
    if DV != start:
        start = DV
    DV_topic = '{"timestamp": "2022-04-11 16:52:26.123", "event": "reverse", "start": "'+ str(bool(DV)) + '"}'

    client.publish('AITEK_EVENTS', DV_topic)
    client.loop_stop()
    
    return {'vehicleSpeed':speedVal,
            'cognitiveDistraction': DC,
            'visualDistraction': str(bool(DV)),
            'angry': str(anger),
            'disgust': str(disgust),
            'fear' : str(fear),
            'joy' : str(joy),
            'neutral' : str(neutral),
            'sadness' : str(sadness),
            'surprise' : str(surprise),
            'arousal': str(arousal)
    }

@app.route('/getFTD')
def getFTD():
    global FTD
    return {'ftd':str(round(FTD, 4))}


@app.route('/infotainment')
def infotainmet():
    # app.route('/infotainment')
    client.disconnect()
    return render_template("CarInfotainment.html")


''' @app.route('/get_elementOfDistraction_data')
def get_elementOfDistraction_data():
    data = db.get_elementOfDistraction_data()
    return data '''

''' @app.route('/get_last_10_FTD')
def get_last_10_FTD():
    data = db.get_last_10_FTD()
    return data '''


if __name__ == "__main__":
    #db = Database()
    app.run(use_reloader=False, port=8000, debug=True)
