# Here is an example of an MQTT subscriber command:


    # mosquitto_sub -d -h 10.110.47.29 -p 1883 -u 'sample4@org.sample4' -P welcome -k 60 -t command///req/#

This command subscribes to any topic that starts with command///req/. The -d option enables debug mode, -h specifies the hostname of the MQTT broker, -p specifies the port number, -u specifies the username, -P specifies the password, -k specifies the keep-alive interval in seconds, and -t specifies the topic to subscribe to.

# Here is an example of an MQTT publisher command:


    # mosquitto_pub -d -h 10.110.47.29 -p 1883 -u 'device7@sample7' -P welcome -k 30 -t 'command///res/213command-and-control/200' -m "{\"topic\":\"sample7/device7/things/live/messages/transmission\",\"headers\": {\"correlation-id\": \"command-and-control\",\"content-type\":\"text/plain\"},\"path\":\"/inbox/messages/transmission\",\"value\":\"automatic: false\",\"status\": 200 }"
    
   # steps

1.This command publishes a message to the topic command///res/213command-and-control/200. The -d option enables debug mode, -h specifies the hostname of the MQTT broker, -p specifies the port number, -u specifies the username, -P specifies the password, -k specifies the keep-alive interval in seconds, -t specifies the topic to publish to, and -m specifies the message payload.


2.In MQTT (Message Queuing Telemetry Transport), a wildcard character is a special character used in a topic filter to match one or more levels in a topic hierarchy. MQTT supports two wildcard characters: the + symbol and the # symbol.


3.The + symbol is used to match a single level in a topic. For example, a subscription to the topic sensors/+/temperature would match messages published to topics like sensors/living-room/temperature or sensors/bedroom/temperature, but not sensors/temperature or sensors/living-room/temperature/humidity.


4.The # symbol is used to match any number of levels in a topic. It must be placed at the end of the topic filter and can only be used once in a filter. For example, a subscription to the topic sensors/# would match messages published to topics like sensors/temperature, sensors/living-room/temperature, or sensors/living-room/temperature/humidity.


5.Wildcard characters + and # can be used in topic filters to subscribe to groups of related topics. The + character represents a single level of hierarchy, while the # character represents multiple levels of hierarchy. For example, a client could subscribe to the topic sensors/+/temperature to receive messages from any sensor that publishes temperature data, or it could subscribe to the topic lights/# to receive messages from any light in the system.


6.However, the + character can only be used as a wildcard when it appears in a topic subscription, not in a topic name.


7.When you define a topic name, you cannot use the + character as a regular character. It's considered a reserved character in MQTT and is only used as a wildcard when it appears in a topic subscription.

# example in case of Hono

    # message :-curl -i -X POST -u ditto:ditto -H 'Content-Type: text/plain' --data-raw '{"automatic":true}' http://192.168.39.202:31902/api/2/things/org.panasonic:cooler/inbox/messages/transmission?timeout=60

      The command///req/# topic you used in your mosquitto_sub command is a wildcard topic that matches any MQTT topics that start with "command///req/". This means that any messages published to topics that match this pattern will be received by the mosquitto_sub command.

      In our case, the message  sent with the curl command was published to a topic that matched the "command///req/" pattern, specifically "command///req/org.panasonic:cooler/inbox/messages/transmission". This topic matches the wildcard pattern specified in the mosquitto_sub command, so the message was received.

      If we subscribe to the topic "command///req/+" and then publish a message using the curl command, the message will not be received by the subscriber because the "+" wildcard only matches a single level in the topic hierarchy.

     In other words, the topic "command///req/+" will only match messages that have a single level after "command///req/", but the topic "command///req/#" matches all messages that have any number of levels after "command///req/".

     In our case, the topic "command///req/+" would only match messages published to topics like "command///req/someTopic", but not to "command///req/someTopic/someSubTopic".
     
 # $share wildcard:-
 
Suppose you have two devices, device1 and device2, and you want to subscribe to messages published by both devices using a single subscription. You can achieve this using the $share wildcard as follows:

1)mosquitto_sub -t '$share/myshare/command///req/#' -v

2)mosquitto_pub -t 'command///req/123' -m 'Message from device1'

3)mosquitto_pub -t 'command///req/456' -m 'Message from device2'

The subscriber should receive both messages, as they were published on the shared subscription                                                          


                                                  example:-
*Create a shared subscription:

    # mosquitto_sub -t '$share/myshare/command///req/#' -v

*Send a message using the Things API and receive the response ID and correlation ID:

    # curl -i -X POST -u ditto:ditto -H 'Content-Type: application/json' --data-raw '{"headers": {"correlation-id": "command-and-control"}}' http://localhost:8080/api/2/things/org.example:myThing/inbox/messages/transmission?timeout=60
   
# Response:
# HTTP/1.1 202 Accepted
# Content-Type: application/json;charset=UTF-8
# iothub-accept: application/json
# iothub-messageid: 4b3389e9-1b8d-4bf5-94a5-5a5d5e95d57e
# iothub-statuscode: 202
# iothub-sequencenumber: 0
# iothub-expiry: 0
# iothub-routing-partition-id: 0
# iothub-enqueuedtime: 2022-04-08T09:26:57.975Z
# iothub-correlationid: command-and-control

*Use the response ID and correlation ID in a message published to the shared subscription:

    # mosquitto_pub -t '$share/myshare/command///res/org.example:myThing/200' -m '{"topic":"org.example:myThing/inbox/messages/transmission","headers":{"correlation-id":"command-and-control"},"path":"/inbox/messages/transmission","value":"{\"temperature\": 25}","status":200}'

*Publish from another device to the shared subscription:

    # mosquitto_pub -t '$share/myshare/command///res/org.example:myOtherThing/200' -m '{"topic":"org.example:myOtherThing/inbox/messages/transmission","headers":{"correlation-id":"command-and-control"},"path":"/inbox/messages/transmission","value":"{\"temperature\": 28}","status":200}'

*When subscribing to the shared subscription, both messages from org.example:myThing and org.example:myOtherThing will be received by the subscriber.

