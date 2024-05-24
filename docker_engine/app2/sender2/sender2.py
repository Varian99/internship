import paho.mqtt.client as mqtt
import os

log_file_path = "/app/logs/output2.log"

def on_message(client, userdata, msg):
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            existing_content = f.read()
    else:
        existing_content = ''
    with open(log_file_path, 'w') as f:
        print(existing_content+ '\n' + msg.topic + " | " + str(msg.payload), file=f)

def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe("app2/sender2")
    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1883)
client.loop_forever()