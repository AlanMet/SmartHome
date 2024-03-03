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
        super().__init__()
        self.consumptionRate = rate

    def getConsumptionRate(self):
        return self.consumptionRate
    
    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"Plug: {switch}, consumption: {self.consumptionRate}"

class SmartFridge(SmartDevice):
    def __init__(self, temp):
        super().__init__()
        self.temps = [1, 3, 5]
        if temp in self.temps:
            self.temperature = temp
        else:
            #default value from the document
            self.temperature = 3

    def getTemperature(self):
        return self.temperature
    
    def setTemperature(self, temp):
        if temp in self.temps:
            self.temperature = temp

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"Fridge: {switch}, Temperature: {self.temperature}"
    

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

    def removeDeviceAt(self, index):
        del self.devices[index]

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
        output = "Devices: \n"
        for device in self.devices:
            output += device.__str__() + "\n"
        return output


def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    plug.setConsumptionRate(50)
    print(plug.getConsumptionRate())
    print(plug)

def testSmartFridge():
    fridge = SmartFridge()
    fridge.toggleSwitch()
    print(fridge.getSwitchedOn())
    print(fridge.getTemperature())
    fridge.setTemperature(7)
    print(fridge.getTemperature())
    print(fridge)

def testSmartHome():
    home = SmartHome()
    plug1 = SmartPlug(45)
    plug2 = SmartPlug(45)
    fridge = SmartFridge()
    plug1.toggleSwitch()
    plug1.setConsumptionRate(150)
    plug2.setConsumptionRate(25)
    fridge.setTemperature(7)
    home.addDevice(plug1)
    home.addDevice(plug2)
    home.addDevice(fridge)
    home.getDeviceAt(1).toggleSwitch()
    print(home)
    home.turnOnAll()
    print(home)


#testSmartPlug()
#testSmartFridge()
#testSmartHome()