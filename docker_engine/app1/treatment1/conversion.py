import paho.mqtt.client as mqtt
import os

log_file_path = "/app/logs/output.log"
log_dir = os.path.dirname(log_file_path)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)
    client.subscribe("app1/conversion")

def on_message(client, userdata, msg):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(log_file_path, 'w') as f:
        value = int(msg.payload)
        print(msg.topic+" | "+str(value)+"°C",file=f)
        data_update = (int(msg.payload) * (9/5)) + 32
    client.publish("app1/encrypt", payload=data_update, qos=0)
    

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1883)
client.loop_forever()