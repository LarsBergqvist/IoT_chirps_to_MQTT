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
            floatVal = self.__rawdata/100.0
            return floatVal
        else:
            return self.__rawdata

