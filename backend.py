class SmartDevice:
    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        if self.switchedOn == True:
            self.switchedOn = False
        else:
            self.switchedOn = True

    def getSwitchedOn(self):
        return self.switchedOn


class SmartPlug(SmartDevice):
    def __init__(self, rate):
        super.__init__()
        self.consumptionRate = rate

    def getConsumptionRate(self):
        return self.consumptionRate
    
    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"plug status: switched {switch}\nconsumption rate: {self.consumptionRate}"


class SmartFridge(SmartDevice):
    def __init__(self):
        super().__init__()
        #default value from the document
        self.temperature = 3

    def getTemperature(self):
        return self.temperature
    
    def setTemperature(self, temp):
        temps = [3, 4, 7]
        if temp in temps:
            self.temperature = temp

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"plug status: switched {switch}\nconsumption rate: {self.temp}"
    

class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices
    
    def getDeviceAt(self, index):
        #if starting from 1 [index-1]
        return self.devices[index]
    
    def addDevice(self, device):
        self.devices.append(device)

    def toggleSwitch(self, index):
        self.devices[index].toggleSwitch()

    def turnOnAll(self):
        for device in self.devices:
            if not device.getSwitchedOn():
                device.toggleSwitch()

    def turnOffAll(self):
        for device in self.devices:
            if device.getSwitchedOn():
                device.toggleSwitch()

    def __str__(self):
        pass

def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    plug.setConsumptionRate(50)
    print(plug.getConsumptionRate())
    print(plug)


