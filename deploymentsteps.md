# Hono Deployment - from source code

I.Prerequisites:

  1. Install minikube by using link - https://minikube.sigs.k8s.io/docs/start/
	2. After installation start minikube
  
	    minikube start --cpus 2 --memory 8192
      
	3. Install docker if it not installed on your machine 
  
	     https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu
       
	4. Install kubectl command line interface                         —----------https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#install-kubectl-binary-with-curl-on-linux
  
	5. Install helm 
  
	   https://helm.sh/docs/intro/install/
     
	6. Add helm repo 
  
	   helm repo add eclipse-iot https://eclipse.org/packages/charts
     
	7. Install java 17 and maven 3.8.1 
             
II. Clone the hono source code from git repo

git clone https://github.com/eclipse-hono/hono.git

III.Installing the chart

1.Create namespace 
	    kubectl create namespace hono
	2.Go to source code folder i'e hono, build and push by using below command 
	      sudo mvn clean install -Pbuild-docker-image,metrics-prometheus,docker-push-image -Ddocker.registry-name=index.docker.io -Ddocker.image.org-name=xxxxxx -Ddocker.username=xxxxxx -Ddocker.password=xxxxx@123	
Note: Use you own org name and docker credentials in above command
	
IV.Custom images:
1.To pull the custom images from repo create customImages.yaml file inside source                               code folder(hono folder) and enter below values 

honoImagesTag: 2.2.0-SNAPSHOT
deviceRegistryExample:
  mongoDBBasedDeviceRegistry:
    imageName: katkuriramesh/hono-service-device-registry-mongodb
  embeddedJdbcDeviceRegistry:
    imageName: katkuriramesh/hono-service-device-registry-jdbc
authServer:
  imageName: katkuriramesh/hono-service-auth
commandRouterService:
  imageName: katkuriramesh/hono-service-command-router
adapters:
  amqp:
    imageName: katkuriramesh/hono-adapter-amqp
  mqtt:
    imageName: katkuriramesh/hono-adapter-mqtt
  http:
    imageName: katkuriramesh/hono-adapter-http


    	Note: use user orgname instead of katkuriramesh
	2.Enter below command to expose the external ips 
	   minikube tunnel
3. Enter below command to pull the images, build  and deploy it
    		helm install eclipse-hono eclipse-iot/hono -n hono --wait -f customImages.yaml
    	4. verify your deployment by entering the below command and it will return list of pods 
    		kubectl get pods -n hono 
Ditto Deployment :
1. Clone source code from below repo
    https://github.com/eclipse/ditto
2.Build Ditto with Maven:
   Maven clean install 
3.Go to inside ditto folder and enter the following command 
    sh build-images.sh
4.Go to ditto/deployment/docker folder and enter the following command 
   docker-compose up -d

Hono cloud Deployment :

ref link : https://www.eclipse.org/hono/getting-started/

hono.eclipse.org
hono.eclipseprojects.io
ditto.eclipseprojects.io
export REGISTRY_IP=hono.eclipseprojects.io
export HTTP_ADAPTER_IP= hono.eclipseprojects.io
export MQTT_ADAPTER_IP= hono.eclipseprojects.io
export AMQP_NETWORK_IP= hono.eclipseprojects.io

1.Create tenent
 curl -i -X POST http://hono.eclipseprojects.io:28080/v1/tenants
     res: {"id":"3e966097-4196-46d3-a253-b184b3700c4c"}

2.Add device to above tenant and pass above id in url
curl -i -X POST http://hono.eclipseprojects.io:28080/v1/devices/3e966097-4196-46d3-a253-b184b3700c4c
     res : "id":"7c7f4c15-cabc-41ef-a747-472b8d8f73d3"}

3.Setting a Password for the Device
curl -i -X PUT -H "content-type: application/json" --data-binary '[{
  "type": "hashed-password",
  "auth-id": "7c7f4c15-cabc-41ef-a747-472b8d8f73d3",
  "secrets": [{
      "pwd-plain": "welcome@123"
  }]
}]' http://hono.eclipseprojects.io:28080/v1/credentials/3e966097-4196-46d3-a253-b184b3700c4c/7c7f4c15-cabc-41ef-a747-472b8d8f73d3


4.Download client and run below command from directory:
	use this link to download client : https://www.eclipse.org/downloads/download.php?file=/hono/hono-cli-1.12.1-exec.jar

	java -jar hono-cli-*-exec.jar --hono.client.host=hono.eclipseprojects.io --hono.client.port=15672 --hono.client.username=consumer@HONO --hono.client.password=verysecret --spring.profiles.active=receiver --tenant.id=impressico


5.Publishing Telemetry Data to the HTTP Adapter
	curl -i -u 7c7f4c15-cabc-41ef-a747-472b8d8f73d3@3e966097-4196-46d3-a253-b184b3700c4c:welcome@123 -H 'Content-Type: application/json' --data-binary '{"temp": 5}' http://hono.eclipseprojects.io:8080/telemetry


6.Publishing Events to the HTTP Adapter
  curl -i -u 7c7f4c15-cabc-41ef-a747-472b8d8f73d3@3e966097-4196-46d3-a253-b184b3700c4c:welcome@123 -H 'Content-Type: application/json' --data-binary '{"alarm": "fire"}' http://hono.eclipseprojects.io:8080/event

7.Install mosquitto broker by using below link
   https://www.vultr.com/docs/install-mosquitto-mqtt-broker-on-ubuntu-20-04-server/

8.Publishing Telemetry Data to the MQTT Adapter
   mosquitto_pub -h hono.eclipseprojects.io -u 7c7f4c15-cabc-41ef-a747-472b8d8f73d3@3e966097-4196-46d3-a253-b184b3700c4c -P welcome@123 -t telemetry -m '{"temp": 5}'

9.Publishing Events to the MQTT Adapter
   mosquitto_pub -h hono.eclipseprojects.io -u 7c7f4c15-cabc-41ef-a747-472b8d8f73d3@3e966097-4196-46d3-a253-b184b3700c4c -P welcome@123 -t event -q 1 -m '{"alarm": "fire"}'




