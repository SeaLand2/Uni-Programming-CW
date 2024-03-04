from tkinter import *
from backend import *


class SmartDeviceWidget:

    def __init__(self, win, mainFrame, device, row):
        self.win = win
        self.mainFrame = mainFrame
        self.device = device
        self.row = row

        self.labelVar = StringVar()
        self.lblDevice = Label (self.mainFrame) # configured in render and updateLabel

        # used in SmartHomeSyetem to remove widgets when a device is removed
        self.widgets = []

    def updateLabel(self):
        labelText = ''
        optionText = ''

        if isinstance(self.device, SmartPlug):
            labelText += 'Plug: '
            optionText += f'Consumption rate: {self.device.getConsumptionRate()}'
        else:
            labelText += 'Oven: '
            optionText += f'Temperature: {self.device.getTemperature()}'

        if self.device.getSwitchedOn() == True:
            labelText += 'On, '
        else:
            labelText += 'Off, '    
        
        self.labelVar.set(labelText + optionText)
        self.lblDevice.config(text=self.labelVar.get())

    def toggleSwitch(self):
        self.device.toggleSwitch()
        self.updateLabel()

    def editDeviceOption(self, option, deviceType):
        try:
            option = int(option)
        except:
            option = 0 # default to 0 if user enters a non-integer
        if deviceType == 'SmartPlug':
            self.device.setConsumptionRate(option)
        else:
            self.device.setTemperature(option)

        self.updateLabel()

    def createEditDevicePopup(self):
        deviceType = type(self.device).__name__ # get name of class

        popup = Toplevel(self.win)
        popup.title(f'Edit {deviceType}')
        popup.geometry('300x100')

        deviceOption = StringVar()
        # set default value of deviceOption to the current consumption rate or temperature
        deviceOption.set(self.device.getConsumptionRate() if deviceType == 'SmartPlug' else self.device.getTemperature())
        # calls edit device whenever the spinbox is changed
        deviceOption.trace_add('write', lambda *args: self.editDeviceOption(deviceOption.get(), deviceType)) 

        spnOption = Spinbox (popup, from_=0, to=1, textvariable=deviceOption) # to be configured in if statements
        spnOption.grid(row=0, column=1, sticky=W)

        if deviceType == 'SmartPlug':
            lblDeviceOption = Label (
                popup,
                text='Consumption rate (0-150): '
            )
            lblDeviceOption.grid(row=0, column=0, sticky=W)
            spnOption.config(to=150)
        else:
            lblDeviceOption = Label (
                popup,
                text='Temperature (0-260): '
            )
            lblDeviceOption.grid(row=0, column=0, sticky=W)
            spnOption.config(to=260)

        btnCancel = Button (
            popup,
            text='Cancel',
            command=popup.destroy
        )
        btnCancel.grid(row=1, column=1, sticky=W)

    def render(self):
        # configure the label
        self.updateLabel()
        self.lblDevice.grid(row=self.row, column=0, columnspan=3, sticky=W)

        btnToggleDevice = Button (
            self.mainFrame,
            text='Toggle',
            command=self.toggleSwitch
        )
        btnToggleDevice.grid(row=self.row, column = 4)

        btnEditDevice = Button (
            self.mainFrame,
            text='Edit',
            command=self.createEditDevicePopup
        )
        btnEditDevice.grid(row=self.row, column = 5)

        self.widgets.append(self.lblDevice)
        self.widgets.append(btnToggleDevice)
        self.widgets.append(btnEditDevice)


class SmartHomeSystem:

    def __init__(self, smartHome):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.geometry("500x250")

        self.mainFrame = Frame(self.win)
        self.mainFrame.pack(padx=10, pady=10)

        self.smartHome = smartHome
        self.renderedObjectsDict = {} # device: [widgets]
        self.deviceWidgetsDict = {} # device: SmartDeviceWidget. allows for labels to be updated

    def run(self):
        self.createWidgets()

        # add widgets for any devices already in smart home
        for device in self.smartHome.getDevices():
            self.addDevice(device)

        self.win.mainloop()

    def createWidgets(self):
        btnTurnOnAll = Button (
            self.mainFrame,
            text='Turn On All',
            command=lambda: self.toggleAll('on')
        )
        btnTurnOnAll.grid(row=0, column=0, columnspan=2, sticky=W)

        btnTurnOffAll = Button (
            self.mainFrame,
            text='Turn Off All',
            command=lambda: self.toggleAll('off')
        )
        btnTurnOffAll.grid(row=0, column=4, columnspan=2, sticky=W)

        btnAddDevice = Button (
            self.mainFrame,
            text='Add',
            command=self.createAddDevicePopup
        )
        btnAddDevice.grid(row=1, column=0, sticky=W)
        self.renderedObjectsDict['btnAddDevice'] = [btnAddDevice]

    def toggleAll(self, state):
        if state == 'on':
            self.smartHome.toggleOnAll()
        else:
            self.smartHome.toggleOffAll()

        # make sure the labels are updated
        for device in self.deviceWidgetsDict.keys():
            self.deviceWidgetsDict[device].updateLabel()

    def addDeviceWidgets(self, device, row):
        widgets = []

        deviceWidget = SmartDeviceWidget(self.win, self.mainFrame, device, row)
        deviceWidget.render()

        self.deviceWidgetsDict[device] = deviceWidget

        for widget in deviceWidget.widgets:
            widgets.append(widget)

        # delete button is seperate as the removeDevice function needs to remove from the renderedObjects list
        btnDeleteDevice = Button (
            self.mainFrame,
            text='Delete',
            command=lambda device=device: self.removeDevice(device)
        )
        btnDeleteDevice.grid(row=row, column = 6, sticky=W)
        widgets.append(btnDeleteDevice)

        return widgets

    def createDevice(self, device, option):
        if device == 'plug':
            newDevice =  SmartPlug(option)
        elif device == 'oven':
            newDevice =  SmartOven()
        self.smartHome.addDevice(newDevice)
        return newDevice

    def createAddDevicePopup(self):
        popup = Toplevel(self.win)
        popup.title('Add Device')
        popup.geometry('500x200')

        # Select device type
        lblDeviceType = Label (
            popup,
            text='Device type: '
        )
        lblDeviceType.grid(row=0, column=0, sticky=W)

        deviceType = StringVar()
        plug = Radiobutton (popup, text='Plug', variable=deviceType, value='plug')
        plug.grid(row=0, column=1, sticky=W)

        oven = Radiobutton (popup, text='Oven', variable=deviceType, value='oven')
        oven.grid(row=0, column=2, sticky=W)
        
        plug.select() # default to plug

        # Select device option. Only for plug as oven is defaulted to 0
        lblDeviceOption = Label (
            popup,
            text='Option (Leave blank for Oven, 0-150 for Plug): '
        )
        lblDeviceOption.grid(row=1, column=0, sticky=W)

        deviceOption = IntVar()
        option = Entry(popup, textvariable=deviceOption)
        option.grid(row=1, column=1)

        # create the device and then pass it to addDevice
        btnAddDevice = Button (
            popup,
            text='Add',
            command=lambda: self.addDevice(self.createDevice(deviceType.get(), deviceOption.get()))
        )
        btnAddDevice.grid(row=2, column=0)

        btnCancel = Button (
            popup,
            text='Cancel',
            command=popup.destroy
        )
        btnCancel.grid(row=2, column=1, sticky=W)

    def addDevice(self, device):
        row = len(self.renderedObjectsDict)
        deviceWidgets = self.addDeviceWidgets(device, row)

        self.renderedObjectsDict[device] = deviceWidgets
        
        # set the 'add' button to the last row  
        self.renderedObjectsDict.get('btnAddDevice')[0].grid(row=row+1, column=0) 

    def configureRows(self):
        for index, device in enumerate(self.renderedObjectsDict.keys()):
            for widget in self.renderedObjectsDict[device]:
                widget.grid(row=index)
        # make sure the 'add' button is at the bottom
        self.renderedObjectsDict.get('btnAddDevice')[0].grid(row=len(self.renderedObjectsDict)+1) 

    def removeDevice(self, device):
        self.smartHome.removeDevice(device)

        for widget in self.renderedObjectsDict[device]:
            widget.destroy()

        self.renderedObjectsDict.pop(device)
        self.deviceWidgetsDict.pop(device)

        # reconfigure the rows so no overlapp occurs when adding now devices
        self.configureRows() 


def setUpHome():
    home = SmartHome()

    for index in range(5):
        print(f'Device {index+1}')
        print('1: Add a smart plug\n2: Add a smart oven')
        choice = input('Select an option: ')
        while not choice in ['1','2']:
            print('Invalid option')
            choice = input('Select an option: ')

        if choice == '1':
            rate = input('What is the consumption rate (0-150): ')
            while not rate.isdigit() or int(rate) not in range(0,151):
                print('Invalid consumption rate')
                rate = input('What is the consumption rate (0-150): ')
            device = SmartPlug(int(rate))
        elif choice == '2':
            device = SmartOven()
        
        home.addDevice(device)

    return home


def main():
    home = setUpHome()

    app = SmartHomeSystem(home)
    app.run()
main()