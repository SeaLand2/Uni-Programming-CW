class SmartDevice:

    def __init__(self):
        self.switchedOn = False

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn


class SmartPlug(SmartDevice):

    def __init__(self, rate):
        super().__init__()
        if rate >= 0 and rate <= 150:
            self.consumptionRate = rate

    def getConsumptionRate(self):
        return self.consumptionRate
    
    def setConsumptionRate(self, rate):
        if rate >= 0 and rate <= 150:
            self.consumptionRate = rate

    def __str__(self):
        return f"Smart Plug(Switched on: {self.switchedOn}, Consumtion rate: {self.consumptionRate})"


class SmartOven(SmartDevice):

    def __init__(self):
        super().__init__()
        self.temperature = 0 # 0 - 260

    def getTemperature(self):
        return self.temperature
    
    def setTemperature(self, temperature):
        if temperature >= 0 and temperature <= 260:
            self.temperature = temperature

    def __str__(self):
        return f"Smart Oven(Switched on: {self.switchedOn}, Temperature: {self.temperature})"


class SmartHome:

    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices
    
    def getDeviceAt(self, index):
        return self.devices[index]

    def addDevice(self, device):
        self.devices.append(device)

    def removeDevice(self, device):
        self.devices.remove(device)

    def toggleSwitch(self, index):
        self.devices[index].toggleSwitch()
    
    def toggleOnAll(self):
        for index in range(len(self.devices)):
            if self.devices[index].getSwitchedOn() == False: 
                self.devices[index].toggleSwitch()
    
    def toggleOffAll(self):
        for index in range(len(self.devices)):
            if self.devices[index].getSwitchedOn() == True: 
                self.devices[index].toggleSwitch()

    def __str__(self):
        output = 'Smart House: '
        for index in range(len(self.devices)):
            output += f'\n{index}: {self.devices[index]}'
        return output


def testSmartPlug():
    plug = SmartPlug(45)

    print(plug.getSwitchedOn())
    plug.toggleSwitch()
    print(plug.getSwitchedOn())

    print(plug.getConsumptionRate())
    plug.setConsumptionRate(50)
    print(plug.getConsumptionRate())

    print(plug)
#testSmartPlug()
    

def testSmartOven():
    oven = SmartOven()

    print(oven.getSwitchedOn())
    oven.toggleSwitch()
    print(oven.getSwitchedOn())

    print(oven.getTemperature())
    oven.setTemperature(150)
    print(oven.getTemperature())

    print(oven)
#testSmartOven()
    

def testSmartHome():
    home = SmartHome()
    plug1 = SmartPlug(45)
    plug2 = SmartPlug(45)
    oven = SmartOven()

    plug1.toggleSwitch()
    plug1.setConsumptionRate(150)

    home.addDevice(plug1)
    home.addDevice(plug2)
    home.addDevice(oven)

    home.toggleSwitch(1)
    print(home)

    home.toggleOnAll()
    print(home)
#testSmartHome()