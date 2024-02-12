class SmartPlug:
    def __init__(self, rate):
        self.switchedOn = False
        self.consumptionRate = rate

    def toggleSwitch(self):
        if self.switchedOn == True:
            self.switchedOn = False
        else:
            self.switchedOn = True

    def getSwitchedOn(self):
        return self.switchedOn
    
    def getConsumptionRate(self):
        return self.consumptionRate
    
    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"plug status: switched {switch}\nconsumption rate: {self.consumptionRate}"
    

class SmartFridge:
    temps = {
        3, 4, 7
    }
    def __init__(self, temperature):
        self.switchedOn = False
        if temperature in temps:
            self.temperature = temperature

    def toggleSwitch(self):
        if self.switchedOn == True:
            self.switchedOn = False
        else:
            self.switchedOn = True

    def getSwitchedOn(self):
        return self.switchedOn
    
    def getConsumptionRate(self):
        return self.consumptionRate
    
    def setConsumptionRate(self, rate):
        self.consumptionRate = rate

    def __str__(self):
        switch = "off"
        if self.switchedOn == True:
            switch = "on"

        return f"plug status: switched {switch}\nconsumption rate: {self.consumptionRate}"
    
def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())
    print(plug.getConsumptionRate())
    plug.setConsumptionRate(50)
    print(plug.getConsumptionRate())
    print(plug)

