import time
from paho.mqtt import client as mqtt_client

broker = '119.91.122.58'
port = 1883
topic = "mqttx/pic"
client_id = "PI3"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg = "1ok"
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print("Send {msg} to topic {topic}".format(msg=msg,topic=topic))
    else:
        print("Failed to send message to topic {topic}".format(topic=topic))  


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()