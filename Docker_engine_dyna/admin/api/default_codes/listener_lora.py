import paho.mqtt.client as mqtt
from pyLoRa import LoRa, LoRaMode

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)

def send_value(client,value):
    print("Envoi de la valeur:", value)
    client.publish("PUBLISH_TOPIC", payload=value, qos=0)

lora = LoRa()
lora.set_mode(LoRaMode.RX)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect("mosquitto", 1885, 60)
client.loop_start()
while True:
    packet = lora.receive_packet()
    if packet:
        print("Paquet reçu :", packet)
        send_value(client,packet)
