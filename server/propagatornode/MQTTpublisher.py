import paho.mqtt.client as mqtt
import time

class MQTTpublisher:
    brokerIP = ""
    brokerPort = 0
    def __init__(self,brokerIP,brokerPort):
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort

    def postMessage(self,topic,message):
        print("Publishing message " + message + " on topic " + topic)
        # Initialize the client that should connect to the Mosquitto broker
        client = mqtt.Client()
        connOK=False
        print("Connecting to " + self.brokerIP + " on port " + str(self.brokerPort))
        while(connOK == False):
            try:
                print("try connect")
                client.connect(self.brokerIP, self.brokerPort, 60)
                connOK = True
            except:
                connOK = False
            time.sleep(2)

        client.publish(topic,message)
        print("Publish done")
        client.disconnect()
    