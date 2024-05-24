import paho.mqtt.client as mqtt
import os

data_list = []
log_file_path = "/app/logs/output2.log"
log_dir = os.path.dirname(log_file_path)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)
    client.subscribe("app2/combine")

def on_message(client, userdata, msg):
    global data_list
    value = int(msg.payload)
    data_list.append(value)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(log_file_path, 'w') as f:        
        print(msg.topic+" | "+str(data_list),file=f)    
    if len(data_list) == 4:
        average = sum(data_list) / len(data_list)
        client.publish("app2/sender2", payload=str(average), qos=0)
        data_list = []

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1883)
client.subscribe("app2/combine")
client.loop_forever()
