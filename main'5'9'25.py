import time
from machine import Pin, SoftSPI, ADC, PWM
import screen
import isr as isr
import sys
#import comm
from _thread import start_new_thread


################
###INTERFACE####
################

class Device:
    _state = None

    def __init__(self, state):
        self.setState(state)
        
    
    def setState(self, state):
        print("Setting state to", type(state).__name__)
        self._state = state
        self._state.device = self 

    def run(self):
        print("running")
        self._state.run()


class State:

    def __init__(self,
                 device = None,
                 pins = None,
                 display = None):
        
        self._device = device
        self.pins = pins if pins is not None else self.initPins()
        self.display = display if display is not None else self.initDisplay()

    @property
    def device(self) -> Device:
        return self._device
    
    @device.setter
    def device(self, device: Device) -> None:
        self._device = device

    def initPins(self) -> None:
        self.pins = PinVect()
        print("init pins")
        return self.pins
    
    def initDisplay(self) -> None:
        self.display = screen.Display(ID=0, sda=0, scl=1, rst=2, addr=60)
        print("init Display")
        return self.display

    def run(self) -> None:
        pass

    def doPWM(self) -> None:
        pass

    def readADC(self, pin) -> None:
        readingADC= pin.read_u16()
        return readingADC

    def writeToUSB(self, data) -> None:
            print(data)
            if isr.incrIH.interrupt_flag == 1:
                data = print("stop")
                isr.incrIH.interrupt_flag == 0


    def updateDisplay(self) -> None:
        self.display.clear()
    
    def txtWrite(self,data):
        db = open("data.txt", "w")
        data = str(data)
        db.write(f"{data}\n")
        db.write("writing stuff")
        db.close()
        return 0
    
    def readFromDB():
        pass

################
###PIN OBJECT###
################

class PinVect:

    def __init__(self):

        #pinInits
        self.relayPin = Pin(21, Pin.OUT) #controls surge protector
        #self.scalePin = ADC(26)
        self.highfillPin = Pin(3, Pin.IN) #high fill sensor
        self.lowfillPin = Pin(4, Pin.IN) #low fill sensor
        self.manualPumpPin = 0
        self.temperaturePin = 0
        #self.photoresist_pin = ADC(26)

        self.pins = self.getPins()


    def getPin(self, name):
        pin = self.pins[str(name)]
        return pin

    def getPins(self):
        pins = { "relayPin": self.relayPin,
                #"scalePin" : self.scalePin,
                "highfillPin": self.highfillPin,
                "lowfillPin": self.lowfillPin,
                "manualPumpPin" : self.manualPumpPin,
                "temperaturePin":self.temperaturePin,
        }
        return pins
        
    def setPin(self, pin, value):
        pass

################
#####STATES#####
################

class initState(State):

    def run(self) -> None:

        self.pins.relayPin.value(0)

        self.display.line_out("Initializing buffer...")
        print("Initializing buffer...")
        #self.buffer = comm.Buffer()
        time.sleep(0.2)

        self.display.line_out("Initializing new thread...")
        print("Initializing new thread...")
        #self._thread = start_new_thread(self.buffer.fillBuffer, ())
        time.sleep(0.2)
        self.updateDisplay()



        self.device.setState(waitState(self.device,
                                       self.pins, 
                                       self.display,
                                       
                                        ))
                                        
class testState(State):

    def __init__(self, 
                 device, 
                 pins: PinVect, 
                 display,
                 ) -> None:
        super().__init__(device, 
                         pins, 
                         display
                         )
        self.pins = pins
        self.display = display
        self.data = []
        self.timer = self.startTimer()

    def run(self) -> None:

        self.display.line_out("Test State", line = 0)
        time.sleep_ms(10)
        self.display.clear()

        self.pins.relayPin.value(1)
        self.updateData(self.data)
        

        while self.pins.highfillPin.value() == 1: #consider adding check for low fill pin too to make more fault tolerant

            self.display.line_out(f"{self.pins.highfillPin.value()}", line=0)
            self.display.line_out("Draining", line = 1)
            self.updateData(self.data)
            time.sleep_ms(10)
        
        
        while self.pins.lowfillPin.value() == 1: #consider adding check for high fill pin too to make more fault tolerant
            self.display.line_out(f"{self.pins.lowfillPin.value()}", line=0)            
            self.display.line_out("Draining to low fill line", line = 1)
            time.sleep_ms(10)
            self.updateData(self.data)
        
        while self.pins.lowfillPin.value() == 0:
            self.display.line_out(f"{self.pins.lowfillPin.value()}", line=0)  
            self.display.line_out("press decrIH to stop pump", line = 1)
            time.sleep_ms(10)
            self.updateData(self.data)
            
            if isr.decrIH.interrupt_flag == 1:
                self.updateData(self.data)
                self.pins.relayPin.value(0)
                self.txtWrite(self.data)
                self.device.setState(waitState(self.device,self.pins,self.display))
                isr.decrIH.interrupt_flag = 0
                break


        if isr.decrIH.interrupt_flag == 1:
            self.updateData(self.data)
            self.pins.relayPin.value(0)
            self.txtWrite(self.data)
            self.device.setState(waitState(self.device,
                                       self.pins,
                                       self.display,
                                       
                                       ))
            isr.decrIH.interrupt_flag = 0

        
    def readADC(self, pin) -> None:
        return super().readADC(pin)
    
    def writeToUSB(self, data) -> None:
        return super().writeToUSB(data)
    
    def updateDisplay(self) -> None:
        return super().updateDisplay()

    def startTimer(self) -> None:
        return time.ticks_ms()
        
    def getTimer(self) -> None:
        timerTime = (time.ticks_ms() - self.timer)/1000
        return timerTime
    
    def txtWrite(self,data):
        return super().txtWrite(data)
    
    def updateData(self, data):
        data.append([self.getTimer(),
                            self.pins.highfillPin.value(),
                            self.pins.lowfillPin.value(),
                            self.pins.relayPin.value()
                            ])
        return data

class waitState(State):

    def __init__(self,
                 device,
                 pins,
                 display,
                 ) -> None:
        
        super().__init__(device,
                        pins,
                        display,
                        )
        self.pins = pins
        self.display = display

    def run(self) -> None:
        self.display.clear()
        time.sleep_ms(10)
        self.display.line_out("Wait State", line = 0)
        time.sleep_ms(10)
        self.display.line_out("Press incrIH to start", line = 1)
        if isr.incrIH.interrupt_flag == 1:
            self.device.setState(testState(self.device,
                                            self.pins,
                                            self.display,
                                            ))
            isr.incrIH.interrupt_flag = 0
        
    def readADC(self) -> None:
        return super().readADC()
    
class deinitState(State):

    def run(self) -> None:
        print ("deinit Pins")


################
######MAIN######
################

if __name__ == "__main__":
    device = Device(initState())
    while True:
        device.run()
        


