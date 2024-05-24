import paho.mqtt.client as mqtt
import time
import random

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)

def send_value(client):
    value = random.randint(0, 20)
    print("Envoi de la valeur:", value)
    client.publish("PUBLISH_TOPIC", payload=value, qos=0)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect("mosquitto", 1885, 60)
client.loop_start()
client.publish("PUBLISH_TOPIC", payload=10, qos=0)
while True:
    send_value(client)
    time.sleep(5)
mqttc.loop_stop()
