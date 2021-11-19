# Sample Java EE 7 - JMS 

This sample uses simplified API of JMS2.0. It contains couple of servlets for performing Point to Point messaging.The JMS Servlet provides means to send/receive messages to a queue.

This sample requires that you create some resources before you deploy the application. 

## 1. Create WAS and MQ instances
  You need to have a WebSphere Application Server (WAS) instance and a IBM MQ queue manager instance for testing the scenario. I'll use docker to quickly get a Websphere Application Server instance and MQ queue manager instance running to demonstrate the steps but you can always use the traditional way to get them running.

  ```bash
    # Create a docker network that was and mq containers are going to sit in 
    docker network create was-jms-mq

    # Create the WAS container
    echo abc1234 > /tmp/waspass # This is the admin password for WAS
    docker run --network was-jms-mq --name was -h was -v /tmp/waspass:/tmp/PASSWORD -p 9043:9043 -p 9443:9443 -d ibmcom/websphere-traditional:latest

    # Create MQ container
    docker run --network was-jms-mq --name mq --env MQ_DEV=false --env LICENSE=accept --env MQ_QMGR_NAME=JMSQM1 -p 1414:1414 -p 9444:9443 --detach -h mq ibmcom/mq
```
  Now you should be able to access WAS console on port 9043 and MQ console 9444 on the machine you are running docker.

## 2. Create the resources required for JMS communication on IBM MQ queue manager and WAS server 
  ### 2.1. Create MQ resources

  Copy the required scripts to the docker container
  ```bash
    docker cp scripts/mq mq:/scripts
  ```

  Create the required users and groups and all the required resources
  ```bash
  # Start a shell in the container as root 
  docker exec -u root -it mq bash

  cd /scripts
  chmod +x /scripts/*
  
  # Create user app and the group mqclient
  ./create-users-groups.sh

  # Create TLS certificate
  ./gen-tls-keydb.sh JMSQM1

  # Exit the root shell
  exit

  # Start a shell as the mq admin user (mqm in most cases)
  docker exec -it mq bash

  # Cd into /scripts
  cd /scripts

  # Create queue manager resources
  runmqsc JMSQM1 < mq-dev-config.mqsc

  # Grant the required permission
  ./grant-permission.sh

  # Exit the shell
  exit
  ```
### 2.2. Create WAS resources
Copy required scripts into the docker container
```bash
docker cp scripts/was was:/scripts
```

Create the required resources
```bash
# Start a shell inside the container
docker exec -it was bash

# Cd into the WAS profile's bin directory
cd /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin

# Create the resources using wsadmin scripting client
./wsadmin.sh -user wsadmin -password abc1234 -f /scripts/createMQJMSResources.py DefaultCell01 DefaultNode01 server1

# Exit the shell
exit

```

You should now be able to see the created resouces in WAS admin console. Take a look to examine them.

## 3. Package and deploy the application
First, examine the code yourself to see what it's doing.
   
Package and deploy the application to WAS server
```bash
# Package the application
mvn clean package

# Copy the war file to the docker container
docker cp target/sample.javaee7.jms.war was:/tmp/

# Start a shell inside the container
docker exec -it was bash

# Cd into the WAS profile's bin directory
cd /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin

# Deploy and start the application using wsadmin scripting client
./wsadmin.sh -user wsadmin -password abc1234 -f /scripts/installApplication.py DefaultCell01 DefaultNode01 server1 /tmp/sample.javaee7.jms.war

# Exit the shell
exit
```

Access the application on https://\<docker-machine-ip\>:9443/sample.javaee7.jms (Ex: https://localhost:9443/sample.javaee7.jms) and test!

## Notice

© Copyright IBM Corporation 2015, 2017. Contains modifications made by [@IreshMM](https://github.com/IreshMM)

## License

This information contains sample code provided in source code form. You may copy, modify, and distribute these sample programs in any form without payment to IBM for the purposes of developing, using, marketing or distributing application programs conforming to the application programming interface for the operating platform for which the sample code is written. 

Notwithstanding anything to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS AND IBM DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR ECONOMIC CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM SHALL NOT BE LIABLE FOR LOSS OF, OR DAMAGE TO, DATA, OR FOR LOST PROFITS, BUSINESS REVENUE, GOODWILL, OR ANTICIPATED SAVINGS. IBM HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO THE SAMPLE SOURCE CODE.
