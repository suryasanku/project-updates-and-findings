    # cat hono.env

      export REGISTRY_IP=10.106.185.117
      export HTTP_ADAPTER_IP=10.105.1.199
      export MQTT_ADAPTER_IP=10.96.156.179
      export APP_OPTIONS='-H 10.106.78.69 -P 9094 -u hono -p hono-secret --ca-file /tmp/truststore.pem --disable-hostname-verification'

source hono.env
================================================================

@IBS-LAP-309:~/hono$  source hono.env curl -i -X POST http://10.106.185.117:28080/v1/tenants/IBS1

================================================================

@IBS-LAP-309:~/hono$ curl -i -X POST http://10.106.185.117:28080/v1/devices/IBS1/lamp

====================================================================

    # curl -i -X PUT -H "content-type: application/json" --data-binary '[{
      "type": "hashed-password",
      "auth-id": "lamp",
      "secrets": [{
      "pwd-plain": "welcome@123"
       }]
      }]' http://10.106.185.117:28080/v1/credentials/IBS1/lamp


    # java -jar hono-cli-*-exec.jar app -H 10.106.78.69 -P 9094 -u hono -p hono-secret --ca-file /tmp/truststore.pem --disable-hostname-verification consume --tenant IBS1


    # java -jar hono-cli-*-exec.jar app ${APP_OPTIONS} consume --tenant IBS1



curl -i -u lamp@IBS1:welcome@123 -H 'Content-Type: application/json' --data-binary '{"temp": 5}' http://10.105.1.199:8080/telemetry

curl -i -u lamp@IBS1:welcome@123 -H 'Content-Type: application/json' --data-binary '{"Heat": "High"}' http://10.105.1.199:8080/event

mosquitto_sub -v -h 10.96.156.179 -u lamp@IBS1 -P welcome@123 -t command///req/#


curl -i -X POST -H "content-type: application/json" --data-binary '{
  "ext": {
    "messaging-type": "kafka"
  }
}' http://10.106.185.117}:28080/v1/tenants

=====================================================================================

mosquitto_sub -v -h 10.96.156.179 -u lamp@IBS1 -P welcome@123 -t command///req/#

===========================================================

ow --tenant IBS1 --device lamp -n setVolume --payload '{"level": 50}'

=====================================================================
req --tenant IBS1 --device lamp -n setBrightness --payload '{"level": 87}'

=================================================================================
export REQ_ID=10117f669c12-09ef-416d-88c1-1787f894856d
mosquitto_pub -h 10.96.156.179 -u bp@impressico -P welcome@123 -t command///res/${REQ_ID}/200 -m '{"current-level": 87}'


=================================================================
req --tenant impressico --device bp -n setBrightness --payload '{"level": 87}' -r 120


=====================================================================
curl -i -u lamp@IBS1:hono-secret -H 'content-type: application/json' --data-binary '{"temp": 15}' http://10.105.1.199:8080/telemetry

=================================

