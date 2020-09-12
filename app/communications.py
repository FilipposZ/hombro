import paho.mqtt.client as mqtt
import json

class Transceiver():

    def __init__(self, broker_ip, broker_port):
        self.client = mqtt.Client('client')
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(broker_ip, broker_port, 60)
        self.client.publish('/pi', 'Successful Connection from client.')

        # Non blocking waiting for messages
        self.client.loop_start()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+ str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("/client/#")

        # Publish to the host devices the hardware that is connected to them.


    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        pass

    def stop_coms(self):
        print('Stopping communication with the broker.')
        self.client.loop_stop()

    def send(self, device_name, action, payload):
        self.client.publish(f'/{device_name}/{action}', payload)
