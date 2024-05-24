import paho.mqtt.client as mqtt
from scapy.all import *
from scapy.layers.dot11 import Dot11


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)

def send_value(client, value):
    print("Envoi de la valeur:", value)
    client.publish("PUBLISH_TOPIC", payload=value, qos=0)

def handle_packet(pkt, client):
    if pkt.haslayer(Dot11):  # Vérifie s'il s'agit d'un paquet Wi-Fi
        # Récupère les données pertinentes du paquet
        value = pkt.summary()  # Utilisez la méthode appropriée pour extraire les données du paquet
        send_value(client, value)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect("mosquitto", 1885, 60)
client.loop_start()

# Capture le trafic Wi-Fi sur l'interface wlan0 en mode monitor
# (Assurez-vous que votre interface Wi-Fi est en mode monitor)
def capture_wifi():
    sniff(iface="wlan0", prn=lambda pkt: handle_packet(pkt, client))

# Lance la capture du trafic Wi-Fi dans un thread séparé
import threading
wifi_thread = threading.Thread(target=capture_wifi)
wifi_thread.start()
