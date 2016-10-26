#!/usr/bin/env python
from propagatornode.propagatorapplication import PropagatorApplication

if __name__ == '__main__':
    wiringPiPinForReceiver = 2
    brokerIP = "192.168.1.16"
    brokerPort = 1883
    app = PropagatorApplication(wiringPiPinForReceiver,brokerIP,brokerPort)
    app.run()
