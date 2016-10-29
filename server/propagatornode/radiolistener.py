from radiomessage import RadioMessage
from measurementtype import MeasurementType
from pi_switch import RCSwitchReceiver

class RadioListener:
    validMeasurementTypes = []
    previousValue = 0
    numIdenticalValuesInARow = 0
    latestMessage = None
    receiver = RCSwitchReceiver()

    def __init__(self,wiringPiPinForReceiver,validMeasurementTypes):
        wiringPiPinForReceiver
        self.validMeasurementTypes = validMeasurementTypes
        self.receiver.enableReceive(wiringPiPinForReceiver)
    
    def newMessageAvailable(self):

        if self.receiver.available():
            value = self.receiver.getReceivedValue()
            self.latestMessage = self.getMessageFromDecodedValue(value)
            self.receiver.resetAvailable()

            if (self.latestMessage is None):
                return False
            else:
                return True

    def getMessageFromDecodedValue(self,value):
        if value == self.previousValue:
            self.numIdenticalValuesInARow += 1
        else:
            self.numIdenticalValuesInARow = 1

        # decode byte3
        byte3 = (0xFF000000 & value) >> 24
        typeID = int((0xF0 & byte3) >> 4)
        seqNum = int((0x0F & byte3))

        # decode byte2 and byte1
        data = int((0x00FFFF00 & value) >> 8)

        # decode byte0
        checkSum = int((0x000000FF & value))

        # calculate simple check sum
        calculatedCheckSum = 0xFF & (typeID + seqNum + data)

        # Sanity checks on received data
        correctData = True
        if calculatedCheckSum != checkSum:
            correctData = False
        elif seqNum > 15:
            correctData = False

        message = None
        if correctData:
            self.previousValue = value
            if self.numIdenticalValuesInARow == 2:
                # only store a value if an identical value was detected twice
                # if detected more than two times, ignore the value        
                measurementType = self.getMeasurementTypeFromId(typeID)
                if measurementType is None:
                    # invalid typeID
                    print("Invalid type id")
                    self.latestMessage = None
                else:
                    message = RadioMessage(measurementType, data)
        
        return message

    def getMeasurementTypeFromId(self,typeID):
        for type in self.validMeasurementTypes:
	    if (type.id == typeID):
                return type

        return None
    
    def getLatestMessage(self):
        return self.latestMessage
