                                               # understanding connection API
                                               
When opening a connection a ConnectionOpenedAnnouncement will be published.
                                      connectivity.commands:openConnection
                                      
When gracefully closing a connection a ConnectionClosedAnnouncement will be published.
                                      connectivity.commands:closeConnection
                                      
This command resets the connection metrics - all metrics are set to 0 again.                                
                                      connectivity.commands:resetConnectionMetrics
                                      
connectivity.commands:enableConnectionLogs
connectivity.commands:resetConnectionLogs

"source" refers to the device or system that provides the data or information, while "target" refers to the device or system that receives the data or information. The "source" and "target" can be any type of physical or virtual device connected to the Internet of Things (IoT). The source and target may be different protocols, data formats or APIs, and Eclipse Ditto provides an integration layer to translate between these and to make it possible to forward the data between them.

  
  
# with single tenant

creating first tenant org.panasonic

now adding device to this particular tenant (cooler)

now add credentials to this device 

                                                # connection types
 # 3 connections:-
                                            
               add connection  (by giving only teleemtry)
                        id:-hono-ditto-panasonictelemetry
               add connection(by giving only event)
                        id:-hono-ditto-panasonicevent
               add connection(by giving only command response)
                        id:-hono-ditto-panasoniccommandresponse
                        
create a policy

 "policyId": "tenant:device"
 
now create thing

      "thingId": "org.panasonic:cooler"
      
# lets check mqtt pub sub

   1.Create command subscriber (SIMULATING DEVICE)
   
        mosquitto_sub -d -h  10.110.47.29 -p 1883 -u 'sample4@org.sample4' -P welcome -k 60 -t command///req/#
         mosquitto_sub -d -h  10.110.47.29 -p 1883 -u 'sample5@org.sample5' -P welcome -k 60 -t command///req/#
           mosquitto_sub -d -h  10.110.47.29 -p 1883 -u 'device7@sample7' -P welcome -k 60 -t command///req/#
        
         // mosquitto_sub -d -h 10.97.236.136 -p 1883 -u 'demo-device@org.eclipse.packages.c2e' -P demo-secret -k 60 -t command///req/#
         

  2.Send a message via Things API (from application)
    
        curl -i -X POST -u ditto:ditto -H 'Content-Type: text/plain' --data-raw '{"automatic":true}' http://192.168.39.202:31902/api/2/things/org.panasonic:cooler/inbox/messages/transmission?timeout=60
        

  3.will receive the command message in #1 command window 
  

  4.Send the response from device back to the cloud services (message back to application)
  
      # mosquitto_pub -d -h 10.110.47.29 -p 1883 -u 'sample4@org.sample4' -P welcome -k 30 \
-t 'command///res/213command-and-control/200' \
-m "{\"topic\":\"org.sample4/sample4/things/live/messages/transmission\",
\"headers\": {\"correlation-id\": \"command-and-control\",
\"content-type\":\"text/plain\"},
\"path\":\"/inbox/messages/transmission\",
\"value\":\"automatic: false\",
\"status\": 200 }"

    # mosquitto_pub -d -h 10.110.47.29 -p 1883 -u 'device7@sample7' -P welcome -k 30 \
-t 'command///res/213command-and-control/200' \
-m "{\"topic\":\"sample7/device7/things/live/messages/transmission\",
\"headers\": {\"correlation-id\": \"command-and-control\",
\"content-type\":\"text/plain\"},
\"path\":\"/inbox/messages/transmission\",
\"value\":\"automatic: false\",
\"status\": 200 }"


# with multiple tenants:-
                                           i have created two tenants org.sample4,org.sample5.
hitting the connection api only once for aloowing both these tenants to do command response.

checked command_response by creating connection for two tenants at a time and checked its working.


                                     #should check whether its possible for more tenants than 2:-
                                    



    # {
        "targetActorSelection": "/system/sharding/connection",
        "headers": {
            "aggregate": false
        },
        "piggybackCommand": {
            "type": "connectivity.commands:createConnection",
            "connection": {
                "id": "hono-ditto-common",
                "name": "hono-ditto-common",
                "connectionType": "kafka",
                "connectionStatus": "open",
                "uri": "ssl://ditto-c2e:verysecret@c2e-kafka:9092",
                "sources": [
                    {
                        "addresses": [
                            "hono.command_response"
                        ],
                        "consumerCount": 1,
                        "qos": 0,
                        "authorizationContext": [
                            "pre-authenticated:hono-connection"
                        ],
                        "enforcement": {
                            "input": "{{ header:device_id }}",
                            "filters": [
                                "{{ entity:id }}"
                            ]
                        },
                        "acknowledgementRequests": {
                            "includes": [],
                            "filter": "fn:delete()"
                        },
                        "headerMapping": {
                            "hono-device-id": "{{ header:device_id }}",
                            "content-type": "{{ header:content-type }}"
                        
                    },
                    "replyTarget": {
                        "address":" hono.command/{{ thing:id }}",
                        "headerMapping": {
                            "device_id": "{{ thing:id }}",
                            "subject": "{{ header:subject | fn:default(topic:action-subject) | fn:default(topic:criterion) }}-response",
                            "correlation-id": "{{ header:correlation-id }}"
                        },
                        "expectedResponseTypes": [
                            "response",
                            "error"
                        ],
                        "enabled": true,
                        "limit": 500
                    }
                } 
            ],
            "targets": [
                {
                    "address": "hono.command/{{ thing:id }}",
                    "topics": [
                        "_/_/things/live/commands",
                        "_/_/things/live/messages"
                    ],
                    "authorizationContext": [
                        "pre-authenticated:hono-connection"
                    ],
                    "headerMapping": {
                        "device_id": "{{ thing:id }}",
                        "subject": "{{ header:subject | fn:default(topic:action-subject) }}",
                        "response-required": "{{ header:response-required }}",
                        "correlation-id": "{{ header:correlation-id }}"
                    }
                },
                {
                    "address": "hono.command/{{thing:id}}",
                    "topics": [
                        "_/_/things/twin/events",
                        "_/_/things/live/events"
                    ],
                    "authorizationContext": [
                        "pre-authenticated:hono-connection"
                    ],
                    "headerMapping": {
                        "device_id": "{{ thing:id }}",
                        "subject": "{{ header:subject | fn:default(topic:action-subject) }}",
                        "correlation-id": "{{ header:correlation-id }}"
                    }
                }
            ],
            "clientCount": 1,
            "failoverEnabled": true,
            "validateCertificates": true,
            "processorPoolSize": 1,
            "specificConfig": {
                "saslMechanism": "plain",
                "bootstrapServers": "c2e-kafka:9092",
                "groupId": "_{{ connection:id }}"
            },
            "ca": "-----BEGIN CERTIFICATE-----\nMIICXzCCAgSgAwIBAgIUa42/FS599Wc7DdPDlQ2lKxqSXpEwCgYIKoZIzj0EAwIwUDELMAkGA1UEBhMCQ0ExDzANBgNVBAcMBk90dGF3YTEUMBIGA1UECgwLRWNsaXBzZSBJb1QxDTALBgNVBAsMBEhvbm8xCzAJBgNVBAMMAmNhMB4XDTIyMDYyMjA2MzM1MloXDTIzMDYyMjA2MzM1MlowUzELMAkGA1UEBhMCQ0ExDzANBgNVBAcMBk90dGF3YTEUMBIGA1UECgwLRWNsaXBzZSBJb1QxDTALBgNVBAsMBEhvbm8xDjAMBgNVBAMMBWthZmthMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEEr76VzDj41w4Q/v8xuBxMJJpkHZaVzFHUHv05G2Em7IGVXJX3YDxiPozV984gOOgjHjqlYpglA6WtWy6FPkG6aOBuDCBtTAdBgNVHQ4EFgQUipGlLxpw3qBqOGbmPvNSHl2BC8YwCwYDVR0PBAQDAgOoMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjBHBgNVHREEQDA+ghUqLmhvbm8ta2Fma2EtaGVhZGxlc3OCGiouaG9uby1rYWZrYS1oZWFkbGVzcy5ob25vgglsb2NhbGhvc3QwHwYDVR0jBBgwFoAUr/zExcFn/Jf7gFFB5oiwcFUb0QMwCgYIKoZIzj0EAwIDSQAwRgIhANxDsUydey3KmprMe2n2cmiMWXwJqag/h+KMoLrZk9S7AiEAspZFzsmxMQF8au/EYhNYj0WNC+8ppfclq+/305IdjYU=\n-----END CERTIFICATE-----\n-----BEGIN CERTIFICATE-----\nMIICAzCCAaqgAwIBAgIUX+WweYPJIpFc0h6IWR3GP9OZy2UwCgYIKoZIzj0EAwIwUjELMAkGA1UEBhMCQ0ExDzANBgNVBAcMBk90dGF3YTEUMBIGA1UECgwLRWNsaXBzZSBJb1QxDTALBgNVBAsMBEhvbm8xDTALBgNVBAMMBHJvb3QwHhcNMjIwNjIyMDYzMzUxWhcNMjMwNjIyMDYzMzUxWjBQMQswCQYDVQQGEwJDQTEPMA0GA1UEBwwGT3R0YXdhMRQwEgYDVQQKDAtFY2xpcHNlIElvVDENMAsGA1UECwwESG9ubzELMAkGA1UEAwwCY2EwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAQibox+SuGA+v+8lUk2h8E5Kdfko7F27pjAj7V4k2jLnIeo1holfDYg2rUrKYTnvb/4PZfrKTHrsMUN+N0ZE0bLo2AwXjAdBgNVHQ4EFgQUr/zExcFn/Jf7gFFB5oiwcFUb0QMwDwYDVR0TAQH/BAUwAwEB/zALBgNVHQ8EBAMCAQYwHwYDVR0jBBgwFoAUvYFKzeT7EXspPh9JAk1e+iRznsgwCgYIKoZIzj0EAwIDRwAwRAIgDnU+TmCW75NRlpMhy55hrf4SzjSdfJgRVm/jx6R2Rz0CIEPV1ziXdckCh1OBQfajaXnX28YvIV+lGGtIRdZ208dB\n-----END CERTIFICATE-----\n",
            "tags": []
        }
    }
    }
    
    #target limit is 4 
