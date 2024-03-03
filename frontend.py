from backend import * 
from tkinter import * 

class AddSystem:
    def __init__(self, win: Tk, home: SmartHome,  topLayer):
        self.win = Toplevel(win)
        self.win.geometry('250x300')
        self.radio = IntVar()
        self.widgets = []
        self.createWidgets()

    def createWidgets(self):
        self.label = Label(self.win, text="Add Device")
        self.label.grid(row=1, column=2)

        label = Label(self.win, text="Type")
        label.grid(row=2, column=1)
        
        self.widgets.append(Radiobutton(self.win, text="Fridge", variable=self.radio, value="Fridge", command=self.setFridge).grid(row=2, column=2))
        self.widgets.append(Radiobutton(self.win, text="Plug", variable=self.radio, value="Plug", command=self.setPlug).grid(row=2, column=3))    

    def setPlug(self):
        print("Hello")
        pass

    def setFridge(self):
        pass

class Slider:
    def __init__(self, win, row, column, lower, higher, name, default):
        self.win = win
        self.row = row
        self.column = column
        self.lower = lower 
        self.higher = higher
        self.name = name
        self.default = default
        self.consumption = IntVar()
        self.createWidgets()
            
    def createWidgets(self):
        label = Label(self.win, text=self.name)
        label.grid(row=self.row, column=self.column-1)
        self.scale = Scale(self.win, orient=HORIZONTAL, from_=self.lower, to=self.higher, variable=self.consumption, showvalue=0)
        self.scale.grid(row=self.row, column=self.column)

        self.scaleEntry = Entry(self.win, width=5)
        self.scaleEntry.grid(row=self.row, column=self.column+1)
        self.scaleEntry.insert(0, f"{self.default}")

        self.scaleEntry.bind("<KeyRelease>", self.editSlider)
        self.scale.bind("<ButtonRelease-1>", self.editEntry)

    def editSlider(self, event):
        num = self.scaleEntry.get()
        if num.isdigit():
            num = int(num)
            if 0<=num<=150:
                self.consumption.set(num)
            elif num > 150:
                self.consumption.set(150)
                self.scaleEntry.delete(0, END)
                self.scaleEntry.insert(0, self.consumption.get())

    def editEntry(self, event):
        self.scaleEntry.delete(0, END)
        self.scaleEntry.insert(0, self.consumption.get())

    def getSliderValue(self):
        return self.consumption.get()
    
    def clearSlider(self):
        self.scale.destroy()
        self.scaleEntry.destroy()
    
class Radio:
    def __init__(self, win, row, column, name, values):
        self.win = win
        self.row = row
        self.column = column
        self.name = name
        self.values = values
        self.checkType()
        self.widgets = []
        self.createWidgets()

    #needed to make the radio for add page but not possible as result of acting differently 
    def checkType(self):
        for x in self.values:
            if type(x) == str:
                self.radio = StringVar()
                return
        self.radio = IntVar()

    def createWidgets(self):
        label = Label(self.win, text=self.name)
        label.grid(row=self.row, column=self.column-1)
        for x in range(0, len(self.values)):
            self.widgets.append(Radiobutton(self.win, text=str(self.values[x]), variable=self.radio, value=self.values[x]).grid(row=self.row, column=self.column+x))
    
    def getRadioValue(self):
        return self.radio.get()
    
    def clearRadio(self):
        for x in self.widgets:
            x.destroy()

class EditSystem:
    def __init__(self, win: Tk, smartObject, topLayer):
        self.win = Toplevel(win)
        self.win.geometry('250x75')
        self.smartObject = smartObject
        self.objectType = str(type(self.smartObject).__name__)
        self.createWidgets()
        self.topLayer = topLayer

    def createWidgets(self):
        label = Label(self.win, text=self.objectType)
        label.grid(row=1, column=2)
        if self.objectType == "SmartFridge":
            self.radio = Radio(self.win, 2, 2, "Temperature", [1, 3, 5])
        else:
            self.slider = Slider(self.win, 2, 2, 0, 150, "Consumption", self.smartObject.getConsumptionRate())
        submitButton = Button(self.win, text="Submit", command=self.submit)
        submitButton.grid(row=3, column=2)

    def submit(self):
        if self.objectType == "SmartFridge":
            self.smartObject.setTemperature(self.radio.getRadioValue())
        else:
            self.smartObject.setConsumptionRate(self.slider.getSliderValue())
        self.win.destroy()
        self.topLayer.createWidgets()

class SmartHomeSystem:
    def __init__(self, home: SmartHome):
        self.home = home
        self.win = Tk()
        self.win.title("Smart Home Interface")
        self.mainFrame = Frame(self.win)
        self.mainFrame.pack()
        self.topWindow = None

        self.rowWidgets = []
        self.sideWidgets = []

    def run(self):
        self.createWidgets()
        self.win.mainloop()
        
    def setSize(self):
        x = 300
        #60 = height of top and bottom row of widgets
        #30 = height of 1 row of widgets
        y = 60+len(self.home.getDevices())*30
        self.win.geometry(f"{x}x{y+10}")

    def createWidgets(self):
        self.deleteAllObjects()
        self.setSize()
        onButton = Button(self.mainFrame, text="Turn on all", width=10, command=self.turnOnAll)
        onButton.grid(row=1, column=1, sticky=W, pady=4)
        self.sideWidgets.append(onButton)

        offButton = Button(self.mainFrame, text="Turn off all", width=10, command=self.turnOffAll)
        offButton.grid(row=1, column=3, columnspan=2, sticky=W, pady=4)
        self.sideWidgets.append(offButton)

        for x in range(len(self.home.getDevices())):
            row=[]
            label = Label(self.mainFrame, text=self.home.getDevices()[x].__str__())
            label.grid(column=1, row=x+2, sticky=W, pady=2)
            row.append(label)

            toggleButton = Button(self.mainFrame, text="Toggle", command = lambda index=x: self.toggleAt(index))
            toggleButton.grid(column=3, row=x+2, sticky=W, pady=2, padx=1)
            row.append(toggleButton)

            editButton = Button(self.mainFrame, text="Edit", command = lambda index=x: self.editWindow(index))
            editButton.grid(column=4, row=x+2, sticky=W, pady=2, padx=1)
            row.append(editButton)

            deleteButton = Button(self.mainFrame, text="Delete", command=lambda index=x: self.deleteRow(index))
            deleteButton.grid(column=5, row=x+2, sticky=W, pady=2, padx=1)
            row.append(deleteButton)

            self.rowWidgets.append(row)

        addButton = Button(self.mainFrame, text="Add", width=10, command=self.addWindow)
        addButton.grid(column=1, row=len(self.home.getDevices())+2, sticky=W, pady=4)
        self.sideWidgets.append(addButton)
        
    def turnOnAll(self):
        self.home.turnOnAll()
        self.createWidgets()
        
    def turnOffAll(self):
        self.home.turnOffAll()
        self.createWidgets()

    def toggleAt(self, index):
        self.home.toggleSwitch(index)
        self.createWidgets()

    def deleteRow(self, index):
        self.home.removeDeviceAt(index)
        self.createWidgets()

    def getSize(self):
        print("The width of Tkinter window:", self.win.winfo_width())
        print("The height of Tkinter window:", self.win.winfo_height())

    def editWindow(self, index):
        #makes sure only 1 edit window can be opened
        if not self.topLevelExists():
            self.topWindow = EditSystem(self.win, self.home.getDeviceAt(index), self)

    def addWindow(self):
        if not self.topLevelExists():
            self.topWindow = AddSystem(self.win, self.home, self)

    def topLevelExists(self):
        try:
            if not self.windowEdit.win.winfo_exists():
                return False
        except AttributeError:
            return False

    def deleteAllObjects(self):
        for row in self.rowWidgets:
            for widget in row:
                widget.destroy()
        for widget in self.sideWidgets:
            widget.destroy()
        self.sideWidgets = []
        self.customerWidgets = []

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

    return home

def main():
    home = setUpHome2()
    app = SmartHomeSystem(home)
    app.run()

main()
