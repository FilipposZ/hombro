import paho.mqtt.client as mqtt

broker_ip = '192.168.1.10'
broker_port = 1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/laptop")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client('Laptop')
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, broker_port, 60)
client.publish('/pi', 'Successful Connection from client.')

# Non blocking waiting for messages
client.loop_start()

def stop_coms():
    print('Stopping communication with the broker.')
    client.loop_stop()

def send(device_name, action, payload):
    client.publish(f'/pi/{device_name}/{action}', payload)
