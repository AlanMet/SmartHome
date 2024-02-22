from backend import * 
from tkinter import * 

class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.home = home
        self.win = Tk()
        self.win.title("Smart Home Interface")
        self.mainFrame = Frame(self.win)
        self.mainFrame.pack(padx=10, pady=10)

    def run(self):
        self.setSize()
        self.createWidgets()
        self.win.mainloop()
        

    def setSize(self):
        x = 500
        y = len(self.home.getDevices())*50
        self.win.geometry(f"{x}x{y}")

    def createWidgets(self):
        onButton = Button(self.mainFrame, text="Turn on all", )
        onButton.pack(side="left", padx=10)

        offButton = Button(self.mainFrame, text="Turn off all",)
        offButton.pack(side="right", padx=10)

        for device in self.home.getDevices():
            label = Label(self.mainFrame, text=device.__str__())
            label.pack()
            
def setUpHome():
    home = SmartHome()
    for x in range(5):
        devicetype = -1
        while devicetype!=1 and devicetype!=2: 
            devicetype = int(input("Would you like to add a plug or fridge? (1 or 2): "))
            if devicetype!=1 and devicetype!=2: 
                print("Please try again")

        if devicetype == 1:
            value = int(input("what is the consumption rate?: "))
            home.addDevice(SmartPlug(value))
        if devicetype == 2:
            value = int(input("what is the temperature?: "))
            home.addDevice(SmartFridge(value))
    return home

def setUpHome2():
    home = SmartHome()
    for x in range(5):
        home.addDevice(SmartPlug(45))

    return home

def main():
    home = setUpHome2()
    app = SmartHomeSystem(home)
    app.run()

main()



