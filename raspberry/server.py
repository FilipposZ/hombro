import paho.mqtt.client as mqtt
import hardware

broker_ip = '192.168.1.10'
broker_port = 1883
config = '' # Is instantiated  in main.py

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))

    client.subscribe("/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # Get the device and the corresponding action to perform
    device_name, action_type = msg.topic.split('/')[1:3]
    action_value = msg.payload.decode()

    if action_type == 'config':
        device = eval(action_value)
        type = device.pop('type')
        hardware.devices[device['name']] = hardware.dev_factory(type, **device)
    elif action_type == 'power':
        hardware.devices[device_name].set_power(action_value)
    elif action_type == 'color':
        hardware.devices[device_name].set_color(*eval(action_value))
    elif action_type == 'mode':
        hardware.devices[device_name].set_mode(action_value)


client = mqtt.Client('pi')
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, broker_port, 60)

client.loop_start()

def stop_coms():
    client.loop_stop()
