#
# A propagator node in an MQTT System
# It listens on messages/chirps via 433MHz radio and translates them to
# MQTT packages that are published over TCP/IP to a broker
#

from measurementtype import MeasurementType
from MQTTpublisher import MQTTpublisher
from radiolistener import RadioListener
import time

class PropagatorApplication:

    wiringPiPinForReceiver = 2
    brokerIP = ""
    brokerPort = 1883

    def __init__(self,wiringPiPinForReceiver,brokerIP,brokerPort):
        self.wiringPiPinForReceiver = wiringPiPinForReceiver
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort    
        
    def run(self):
        # Defines the radio listener that uses pi-switch to listen to messages
        # over 433 MHz radio
        validMeasurementTypes = [ 
            MeasurementType(1,"Temp","float","Home/TopFloor/Temperature"),
            MeasurementType(2,"Pressure(hPa)","int","Home/TopFloor/Pressure"),
            MeasurementType(3,"DoorOpened","int","Home/FrontDoor/Status")
            ]

        radioListener = RadioListener(self.wiringPiPinForReceiver,validMeasurementTypes)

        # Defines the publisher that publishes MQTT messages to a broker
        publisher = MQTTpublisher(self.brokerIP,self.brokerPort)

        while True:
            if radioListener.newMessageAvailable():
                message = radioListener.getLatestMessage()
                if message is not None:
                    # Take the radio message and publish the data as an MQTT message
                    publisher.postMessage(message.getTopic(),str(message.getValue()))

            time.sleep(1)
