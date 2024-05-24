import paho.mqtt.client as mqtt
import bluetooth

# Il faudra peut être faire exécuter cette commande au conteneur sudo apt install libbluetooth-dev
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connecté au broker MQTT avec le code de retour:", reason_code)

def send_value(client,value):
    print("Envoi de la valeur:", value)
    client.publish("PUBLISH_TOPIC", payload=value, qos=0)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = "PORT_NUMBER" 
server_sock.bind(("", port))
server_sock.listen(1)
client_sock, client_info = server_sock.accept()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect("mosquitto", 1885, 60)
client.loop_start()
client.publish("PUBLISH_TOPIC", payload=10, qos=0)
try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        send_value(client,data)
finally:
    client_sock.close()
    server_sock.close()

