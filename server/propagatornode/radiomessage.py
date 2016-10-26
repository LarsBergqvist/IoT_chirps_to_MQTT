from measurementtype import MeasurementType

class RadioMessage:
    __rawdata = 0
    __measurementType = None

    def __init__(self,measurementType,measurementValue):
        self.__rawdata = measurementValue
        self.__measurementType = measurementType

    def getName(self):
        if (self.__measurementType is None):
            return ""
        return self.__measurementType.name
    
    def getTopic(self):
        if (self.__measurementType is None):
            return ""
        return self.__measurementType.topic

    def getValue(self):
        if (self.__measurementType is None):
            return 0
        if self.__measurementType.type == "float":
            # Handle float values that can be negative from -327.67 to +327.67
            # Bit 15 contains the sign flag,
            # the rest of the word (max 0x7FFF) contains the float value * 100
            data = self.__rawdata
            floatResult = 0.0
            if (data & 0x8000 > 0):
                # this should be a negative value
                data &=~(1 << 15)
                floatResult = -data
            else:
                data &=~(1 << 15)
                floatResult = data
                
            floatResult = floatResult/100.0            

            return floatResult
        else:
            return self.__rawdata

