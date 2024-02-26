from backend import * 
from tkinter import * 

class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.home = home
        self.win = Tk()
        self.win.title("Smart Home Interface")
        self.leftFrame=Frame(self.win, background="blue")
        self.leftFrame.pack(side="left", expand=True)
        self.rightFrame = Frame(self.win, background="red")
        self.rightFrame.pack(side="right", expand=True)
        self.rightTopFrame = Frame(self.rightFrame, background="green")
        self.rightTopFrame.grid(column=0, row=0)

    def run(self):
        self.setSize()
        self.createWidgets()
        self.win.mainloop()
        
    def setSize(self):
        x = 500
        y = len(self.home.getDevices())*10
        self.win.geometry(f"{x}x{y}")

    def createWidgets(self):
        onButton = Button(self.leftFrame, text="Turn on all")
        onButton.pack()

        offButton = Button(self.rightTopFrame, text="Turn off all")
        offButton.pack()

        print(self.home.devices)
        for x in range(len(self.home.getDevices())):
            label = Label(self.leftFrame, text=self.home.getDevices()[x].__str__())
            label.pack()

            toggleButton = Button(self.rightFrame, text="Toggle")
            toggleButton.grid(column=2, row=x+2, sticky=W, pady=2)

            editButton = Button(self.rightFrame, text="Edit")
            editButton.grid(column=3, row=x+2, sticky=W, pady=2)

            
            deleteButton = Button(self.rightFrame, text="Delete")
            deleteButton.grid(column=4, row=x+2, sticky=W, pady=2)


        addButton = Button(self.leftFrame, text="Add")
        addButton.pack()
        
            
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
    for x in range(3):
        home.addDevice(SmartPlug(150))
    
    home.addDevice(SmartPlug(45))
    home.addDevice(SmartFridge(7))

    print(home.devices)

    return home

def main():
    home = setUpHome2()
    app = SmartHomeSystem(home)
    app.run()

main()



