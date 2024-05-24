import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet
import os

log_file_path = "/app/logs/output.log"
log_dir = os.path.dirname(log_file_path)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)
    client.subscribe("SUBSCRIBE_TOPIC")

def on_message(client, userdata, msg):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            existing_content = f.read()
    else:
        existing_content = ''
    with open(log_file_path, 'w') as f:
        print(existing_content+ '\n' + msg.topic + " | " + str(float(msg.payload)) +"°F", file=f)
    encrypted_data = encrypt_data(str(float(msg.payload)))
    client.publish("PUBLISH_TOPIC", payload=encrypted_data, qos=0)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1885)
client.loop_forever()