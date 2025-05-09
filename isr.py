
import time
from machine import Pin, SoftSPI, ADC, PWM
import screen




#### GUI BUTTONS ####
guiButtonFlags = [False,False,False,False]
curTime = time.ticks_ms()
guiButtonLasts = [curTime,curTime,curTime,curTime] #timestamp of last button toggle   


#### GUI BUTTON IHs ####
#if 200 ms has passed since last assignment for the appropriate flag, set button's flag to true
def incrIH(pin):
    global guiButtonFlags, guiButtonLasts
    curTime = time.ticks_ms()
    guiButtonFlags[0] = time.ticks_diff(curTime, guiButtonLasts[0]) > 200
    guiButtonLasts[0] = guiButtonFlags[0] * curTime + (1-guiButtonFlags[0]) * guiButtonLasts[0]

def backIH(pin):
    global guiButtonFlags, guiButtonLasts
    curTime = time.ticks_ms()
    guiButtonFlags[1] = time.ticks_diff(curTime, guiButtonLasts[1]) > 200
    guiButtonLasts[1] = guiButtonFlags[1] * curTime + (1-guiButtonFlags[1]) * guiButtonLasts[1]

def decrIH(pin):
    global guiButtonFlags, guiButtonLasts
    curTime = time.ticks_ms()
    guiButtonFlags[2] = time.ticks_diff(curTime, guiButtonLasts[2]) > 200
    guiButtonLasts[2] = guiButtonFlags[2] * curTime + (1-guiButtonFlags[2]) * guiButtonLasts[2]

def nextIH(pin):
    global guiButtonFlags, guiButtonLasts
    curTime = time.ticks_ms()
    guiButtonFlags[3] = time.ticks_diff(curTime, guiButtonLasts[3]) > 200
    guiButtonLasts[3] = guiButtonFlags[3] * curTime + (1-guiButtonFlags[3]) * guiButtonLasts[3]



###PIN DEFINITIONS###
#### GUI BUTTONS ####

#### GUI BUTTONS ####
incrButton = Pin(10, Pin.OUT, value=1)
backButton = Pin(11, Pin.OUT, value=1)
decrButton = Pin(12, Pin.OUT, value=1)
nextButton = Pin(13, Pin.OUT, value=1)
incrButton.irq(handler=incrIH, trigger=Pin.IRQ_FALLING)
backButton.irq(handler=backIH, trigger=Pin.IRQ_FALLING)
decrButton.irq(handler=decrIH, trigger=Pin.IRQ_FALLING)
nextButton.irq(handler=nextIH, trigger=Pin.IRQ_FALLING)



#### CHANNEL CTRL IHs ####
#NOTE:
#ch0-ch3 are known as ch1-ch4 outside of the code, this is for ease of interaction with the end-user

#if 500 ms has passed, flip the associated flag's value to opposite of what it was
def ch0IH(pin):
    global chPresetFlags, chPresetLasts
    curTime = time.ticks_ms()
    update = time.ticks_diff(curTime, chPresetLasts[0]) > 500
    chPresetFlags[0] = update * (1-chPresetFlags[0]) + (1-update) * chPresetFlags[0]
    chPresetLasts[0] = update * curTime + (1-update) * chPresetLasts[0]

def ch1IH(pin):
    global chPresetFlags, chPresetLasts
    curTime = time.ticks_ms()
    update = time.ticks_diff(curTime, chPresetLasts[1]) > 500
    chPresetFlags[1] = update * (1-chPresetFlags[1]) + (1-update) * chPresetFlags[1]
    chPresetLasts[1] = update * curTime + (1-update) * chPresetLasts[1]

def ch2IH(pin):
    global chPresetFlags, chPresetLasts
    curTime = time.ticks_ms()
    update = time.ticks_diff(curTime, chPresetLasts[2]) > 500
    chPresetFlags[2] = update * (1-chPresetFlags[2]) + (1-update) * chPresetFlags[2]
    chPresetLasts[2] = update * curTime + (1-update) * chPresetLasts[2]

def ch3IH(pin):
    global chPresetFlags, chPresetLasts
    curTime = time.ticks_ms()
    update = time.ticks_diff(curTime, chPresetLasts[3]) > 500
    chPresetFlags[3] = update * (1-chPresetFlags[3]) + (1-update) * chPresetFlags[3]
    chPresetLasts[3] = update * curTime + (1-update) * chPresetLasts[3]


#### CTRL SIG_IN ####
ch0Signal = Pin(15, Pin.IN)
ch1Signal = Pin(16, Pin.IN)
ch2Signal = Pin(17, Pin.IN)
ch3Signal = Pin(18, Pin.IN)


#### CHANNEL CTRL BUTTONS ####
ch0Button = Pin(3, Pin.OUT, value=1)
ch1Button = Pin(4, Pin.OUT, value=1)
ch2Button = Pin(5, Pin.OUT, value=1)
ch3Button = Pin(14, Pin.OUT, value=1)
ch0Button.irq(handler=ch0IH, trigger=Pin.IRQ_FALLING)
ch1Button.irq(handler=ch1IH, trigger=Pin.IRQ_FALLING)
ch2Button.irq(handler=ch2IH, trigger=Pin.IRQ_FALLING)
ch3Button.irq(handler=ch3IH, trigger=Pin.IRQ_FALLING)