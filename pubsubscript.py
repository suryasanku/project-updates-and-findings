import json

import paho.mqtt.client as mqtt
import requests

responseId = "";
correlationId = "";


# Callback when the client connects to the broker

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("command///req/#")


def on_publish(client, userdata, rc):
    print("on_publish called! {}".format(rc))


def publishData(rid, cid):
    # JSON string
    print(rid, cid)
    body = '{"topic": "org.impressico/oxygen/things/live/messages/temperature","headers":{"correlation-id": "' + cid + '","content-type":"text/plain"}, "path":"/inbox/messages/temperature","value":"value: 300","status": 200}';
    print("command///res/" + rid + "/200", body)
    client.publish("command///res/" + rid + "/200", body)


# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    x = msg.topic
    y = x.split("/")
    print(y);
    # Publish a message
    payloadmsg = str(msg.payload);
    corid = payloadmsg.split(",");
    coridval = corid[20].split(':');
    correlationid = coridval[1][1:-2];
    global responseId
    responseId = y[4];
    global correlationId;
    correlationId = correlationid;
    publishData(responseId, correlationId)

    print(str(msg.payload));
    # print(msg.topic);


# Create a new client instance
client = mqtt.Client()

# Register the callbacks
# 0: Connection successful
# 1: Connection refused - incorrect protocol version
# 2: Connection refused - invalid client identifier
# 3: Connection refused - server unavailable
# 4: Connection refused - bad username or password
# 5: Connection refused - not authorised

client.on_connect = on_connect
client.on_message = on_message
username = "oxygen@org.impressico"
password = "welcome"
client.username_pw_set(username=username, password=password)

# Connect to the broker
client.connect("10.100.192.253", 1883, 60)

# Run the client loop to process incoming events
client.loop_forever()
