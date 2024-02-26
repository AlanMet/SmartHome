from backend import * 
from tkinter import * 

class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.rowWidgets = []
        self.home = home
        self.win = Tk()
        self.win.title("Smart Home Interface")
        self.mainFrame = Frame(self.win)
        self.mainFrame.pack()

    def run(self):
        self.setSize()
        #self.createFrameLayout()
        self.createWidgets()
        self.win.mainloop()
        
    def setSize(self):
        x = 300
        y = len(self.home.getDevices())*43
        self.win.geometry(f"{x}x{y}")

    def createWidgets(self):
        onButton = Button(self.mainFrame, text="Turn on all", width=10, command=self.turnOnAll)
        onButton.grid(row=1, column=1, sticky=W, pady=4)

        offButton = Button(self.mainFrame, text="Turn off all", width=10, command=self.turnOffAll)
        offButton.grid(row=1, column=3, columnspan=2, sticky=W, pady=4)

        for x in range(len(self.home.getDevices())):
            row=[]
            label = Label(self.mainFrame, text=self.home.getDevices()[x].__str__())
            label.grid(column=1, row=x+2, sticky=W, pady=2)
            row.append(label)

            toggleButton = Button(self.mainFrame, text="Toggle")
            toggleButton.grid(column=3, row=x+2, sticky=W, pady=2, padx=1)
            row.append(toggleButton)

            editButton = Button(self.mainFrame, text="Edit")
            editButton.grid(column=4, row=x+2, sticky=W, pady=2, padx=1)
            row.append(editButton)

            deleteButton = Button(self.mainFrame, text="Delete", command=lambda index=x: self.deleteAll(index))
            deleteButton.grid(column=5, row=x+2, sticky=W, pady=2, padx=1)
            row.append(deleteButton)

            self.rowWidgets.append(row)

        addButton = Button(self.mainFrame, text="Add", width=10)
        addButton.grid(column=1, row=len(self.home.getDevices())+2, sticky=W, pady=4)
        
    def turnOnAll(self):
        self.home.turnOnAll()
        

    def turnOffAll(self):
        self.home.turnOffAll()

    def deleteAll(self, index):
        print(index)
        for widget in self.rowWidgets[index]:
            widget.destroy()
        self.home.removeDeviceAt(index)

    

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



