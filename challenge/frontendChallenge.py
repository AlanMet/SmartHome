from backendChallenge import * 
from tkinter import * 
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox

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
        self.label = Label(self.win, text=self.name)
        self.label.grid(row=self.row, column=self.column-1)
        self.scale = ttk.Scale(self.win, orient=HORIZONTAL, from_=self.lower, to=self.higher, variable=self.consumption)
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

    def get(self):
        return self.consumption.get()
    
    def clearSlider(self):
        self.scale.destroy()
        self.scaleEntry.destroy()

    def destroy(self):
        self.label
        self.scale.destroy()
        self.scaleEntry.destroy()
    
class Radio:
    def __init__(self, win, row, column, name, values, commands=None):
        self.win = win
        self.frame = Frame(win)
        self.frame.grid(row=row, column=column+1)
        self.row = row
        self.column = column
        self.name = name
        self.values = values
        self.checkType()
        self.widgets = []
        self.commands=commands
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
        label.grid(row=self.row, column=self.column)
        column = 1
        for x in range(0, len(self.values)):
            radio = Radiobutton(self.frame, text=str(self.values[x]), variable=self.radio, value=self.values[x], command=lambda index=x: self.getCommand(index))
            radio.grid(row=0, column=column)
            column+=1
            self.widgets.append(radio)
    
    def get(self):
        value = self.radio.get()
        return value
    
    def destroy(self):
        for x in self.widgets:
            x.destroy()
        self.frame.destroy()

    def set(self, value):
        self.radio.set(value)

    def getCommand(self, index):
        if self.commands is None:
            return None
        elif len(self.commands) == 1:
            return self.commands[0]()
        else:
            return self.commands[index]()
        

class spinbox:
    def __init__(self, win, start, end, row, column, command=None, parent=None):
        self.win = win
        self.start = start
        self.end = end
        self.command = command
        self.row = row
        self.column = column
        self.createWidgets()

    def createWidgets(self):
            self.box = Spinbox(self.win, from_=self.start, to=self.end, width=5)
            self.box.grid(row=self.row, column=self.column)
            
            self.box.bind("<Return>", self.returnValue)
            self.box.bind("<MouseWheelRealease>", self.returnValue)

    def returnValue(self):
        print("Hello")

class AddSystem:
    def __init__(self, win: Tk, home: SmartHome,  topLayer):
        self.win = Toplevel(win)
        self.home = home
        self.topLayer = topLayer
        self.win.geometry('250x100')
        self.radio = StringVar()
        self.widgets = []
        self.optionWidget = None
        self.option=None
        self.createWidgets()

    def createWidgets(self):
        self.label = Label(self.win, text="Add Device")
        self.label.grid(row=1, column=2)

        radio = Radio(self.win, 2, 1, "Type", ["Fridge", "Plug"], [self.setFridge, self.setPlug])

        submitButton = ttk.Button(self.win, text="Submit", width=10, command=self.submit)
        submitButton.grid(column=2, row=4)

    def setPlug(self):
        self.deleteAll()
        slider = Slider(self.win, 3, 2, 0, 150, "Consumption", 150)
        self.optionWidget = slider
        self.option="Plug"
        
    def setFridge(self):
        self.deleteAll()
        radio = Radio(self.win, 3, 1, "Temperature", [1, 3, 5])
        self.optionWidget = radio
        self.option = "Fridge"

    def submit(self):
        if self.optionWidget is not None:
            value = self.optionWidget.get()
            print(self.radio.get())
            if self.option == "Fridge":
                self.home.addDevice(SmartFridge(value))
            else:
                self.home.addDevice(SmartPlug(value))

            self.topLayer.createWidgets()
            self.win.destroy()

    def deleteAll(self):
        try:
            self.optionWidget.destroy()
            self.optionWidget = None
        except AttributeError:
            return
        
class ScheduleSystem:
    def __init__(self, win: Tk, smartObject, topLayer):
        self.win = Toplevel(win)
        self.win.geometry('200x100')
        self.smartObject = smartObject
        self.objectType = str(type(self.smartObject).__name__)
        self.createWidgets()
        self.topLayer = topLayer

    def createWidgets(self):
        label = Label(self.win, text=self.objectType)
        label.grid(row=1, column=2)

        label2 = Label(self.win, text="Start Time")
        label2.grid(row=2, column=1)
        self.onBox = Spinbox(self.win, from_=1, to=23, width=6)
        if type(self.smartObject.getTurnOn()) is int:
            self.onBox.insert(0, str(self.smartObject.getTurnOn()))
        self.onBox.grid(row=2, column=2, pady=2)

        label3 = Label(self.win, text="End Time")
        label3.grid(row=3, column=1)
        self.offBox = Spinbox(self.win, from_=1, to=23, width=6)
        if type(self.smartObject.getTurnOff()) is int:
            self.offBox.insert(0, str(self.smartObject.getTurnOff()))
        self.offBox.grid(row=3, column=2)

        submitButton = Button(self.win, text="Submit", command=self.submit)
        submitButton.grid(row=4, column=2)

    def submit(self):
        if self.onBox.get() == None or self.offBox.get() == None:
            return
        elif self.onBox.get() == self.offBox.get():
            messagebox.showerror('Value Error', 'Error: Times cannot be the same!')
        else:
            if self.offBox.get() != '':
                self.smartObject.setTurnOff(int(self.offBox.get()))
            if self.onBox.get() != '':
                self.smartObject.setTurnOn(int(self.onBox.get()))
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
        self.time = 0
        self.clockRunning = False
        self.timeVariable = StringVar()
        self.toggleVariable = StringVar()
        self.toggleVariable.set("Turn on all")
        self.rowWidgets = []
        self.sideWidgets = []
        self.colours = ["", "red"]

    def run(self):
        self.createWidgets()
        self.win.mainloop()
        
    def setSize(self):
        x = 400
        y = 60+len(self.home.getDevices())*35
        self.win.geometry(f"{x}x{y+10}")

    def createWidgets(self):
        self.deleteAllObjects()
        self.setSize()
        if not self.clockRunning:
            self.updateTime()
        self.getToggle()
        toggleButton = ttk.Button(self.mainFrame, text=self.toggleVariable.get(), width=10, command=self.toggleAll)
        toggleButton.grid(row=1, column=1, sticky=W, pady=4, columnspan=3)
        self.sideWidgets.append(toggleButton)
        

        for x in range(len(self.home.getDevices())):
            row=[]
            objectType = str(type(self.home.getDevices()[x]).__name__)
            src = self.home.getDevices()[x].getImage()
            picture = PhotoImage(file=src)
            picture = picture.subsample(10, 10)
            button = ttk.Button(self.mainFrame, image=picture, command= lambda index=x: self.toggleAt(index))
            button.image = picture
            button.grid(column=1, row=x+2, sticky=W)
            row.append(button)

            label = Label(self.mainFrame, text=self.home.getDevices()[x].__str__())
            label.grid(column=3, row=x+2, sticky=W, pady=2)
            row.append(label)

            if objectType == "SmartFridge":
                radio = Radio(self.mainFrame, x+2, 4, None, [1, 3, 5], [lambda index=x: self.editFridgeAt(index, radio)])
                radio.set(self.home.getDevices()[x].getTemperature())
                row.append(radio)
            else:
                box = Spinbox(self.mainFrame, from_=0, to=150, width=5, command=lambda index=x: self.editPlugAt(index, box))
                box.set(self.home.getDevices()[x].getConsumptionRate())
                box.grid(row=x+2, column=5)
                row.append(box)

                box.bind("<Return>", lambda event, index=x: self.editPlugAt(index=index, box=box))

            scheduleButton = ttk.Button(self.mainFrame, text="Schedule", command=lambda device = self.home.getDevices()[x]: self.scheduleWindow(device))
            scheduleButton.grid(column=6, row=x+2, sticky=W, pady=2, padx=1)
            row.append(scheduleButton)

            deleteButton = ttk.Button(self.mainFrame, text="Delete", command=lambda index=x: self.deleteRow(index))
            deleteButton.grid(column=7, row=x+2, sticky=W, pady=2, padx=1)
            row.append(deleteButton)

            self.rowWidgets.append(row)

        addButton = ttk.Button(self.mainFrame, text="Add", width=10, command=self.addWindow)
        addButton.grid(column=1, row=len(self.home.getDevices())+2, sticky=W, pady=4, columnspan=3)
        self.sideWidgets.append(addButton)

        timeLabel = Label(self.mainFrame, textvariable=self.timeVariable)
        timeLabel.grid(column=7, row=len(self.home.getDevices())+2)
        self.sideWidgets.append(timeLabel)

        accessButton = Button(self.mainFrame, text="Accessibility", command=self.accessWindow)
        accessButton.grid(column=7, row=1)
        self.sideWidgets.append(accessButton)


    def updateTime(self):
        self.clockRunning = True
        self.time +=1
        if self.time == 24:
            self.time = 1
        self.timeVariable.set(f"{self.time}:00")
        self.updateDevices()
        self.win.after(3000, self.updateTime)

    def updateDevices(self):
        #reduce flashing
        update = False
        for device in self.home.getDevices():
            off = device.getTurnOff()
            on = device.getTurnOn()
            if self.time == on:
                device.setSwitchedOn(True)
                update = True
            if self.time == off:
                device.setSwitchedOn(False)
                update = True
        if update == True:
            self.createWidgets()

    def getToggle(self):
        devices = self.home.getDevices()
        count = 0
        for device in devices:
            if device.getSwitchedOn():
                count+=1

        if count == len(devices):
            self.toggleVariable.set("Turn off all")
        if count == 0:
            self.toggleVariable.set("Turn on all")

    def toggleAll(self):
        if self.toggleVariable.get() == "Turn on all":
            self.toggleVariable.set("Turn off all")
            self.turnOnAll()
        else:
            self.toggleVariable.set("Turn on all")
            self.turnOffAll()
        
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

    def accessWindow(self):
        #makes sure only 1 edit window can be opened
        if not self.topLevelExists():
            print("Access")

    def scheduleWindow(self, device):
        if not self.topLevelExists():
            self.topWindow = ScheduleSystem(self.win, device, self)

    def addWindow(self):
        if not self.topLevelExists():
            self.topWindow = AddSystem(self.win, self.home, self)

    def topLevelExists(self):
        try:
            if not self.topWindow.win.winfo_exists():
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

    def editFridgeAt(self, index, radio):
        device = self.home.getDeviceAt(index)
        device.setTemperature(radio.get())
        self.createWidgets()

    def editPlugAt(self, index, box):
        device = self.home.getDeviceAt(index)
        if int(box.get())<0:
            device.setConsumptionRate(0)
        elif int(box.get())>150:
            device.setConsumptionRate(150)
        else:
            device.setConsumptionRate(int(box.get()))
        self.createWidgets()
        

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
