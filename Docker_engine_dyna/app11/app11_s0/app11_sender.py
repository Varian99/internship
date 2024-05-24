import paho.mqtt.client as mqtt
import os
import pymongo
import requests

mongodb_client = pymongo.MongoClient("mongodb://10.11.0.161:27017/")
# log_file_path = "/app/logs/output.log"
# log_dir = os.path.dirname(log_file_path)
url = 'http://10.11.0.161:5100/'

def on_message(client, userdata, msg):
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    # if os.path.exists(log_file_path):
    #     with open(log_file_path, 'r') as f:
    #         existing_content = f.read()
    # else:
    #     existing_content = ''
    # with open(log_file_path, 'w') as f:
    #     print(existing_content+ '\n' + msg.topic + " | " + str(msg.payload), file=f)
    db = mongodb_client["Temperature"]
    collection = db["Temp_chiffrée"]
    collection.insert_one({"message": msg.payload.decode()})
    response = requests.post(f"{url}/recevoir_donnees", json=msg.payload.decode())

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)
    client.subscribe("app11/encrypt")

db = mongodb_client["Temperature"]
collection = db["Temp_chiffrée"]
documents = collection.find()
# with open("/app/logs/bdd.log", "w") as f:
#     for document in documents:
#         print(str(document), file=f)
        
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1885)
client.loop_forever()