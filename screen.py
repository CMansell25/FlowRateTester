from machine import Pin, I2C
import time

#Made by Allen Larabee
#10/28/2021

#Initialization bytes (and their meanings)
#0x00 ; 0000 0000  ; - ; control byte, no more to follow
#0x39 ; 0011 10[01]; - ; function set, instruction set: 01
#0x14 ; 0001 0100  ; - ; bias set
#0x78 ; 0111 [1000]; - ; contrast set, CR: 1000, range:[2,15]
#0x5e ; 0101 [1110]; - ; power/icon/contrast control, icon: 1, booster: 1, C: 10
#0x6d ; 0110 [1101]; - ; follower control, followerOn: 1, Rab: 101
#0x0f ; 0000 1[111]; c ; display on/off, dispFullOn: 1, cursorOn: 1, cursorPosOn: 1
#0x01 ; 0000 0001  ; - ; clear display
#0x06 ; 0000 01[10]; - ; entry mode set

#Constructor needs:
#ID   = bus id
#sda  = sda pin #
#scl  = scl pin #
#rst  = reset pin #
#addr = 7-bit address in decimal
#freq = scl frequency (Hz), default 200000 Hz

class Display:
    def __init__(self, ID, sda, scl, rst, addr, freq=200000):
        self.id = ID
        self.sda_pin = Pin(sda, Pin.OUT)
        self.scl_pin = Pin(scl, Pin.OUT)
        self.rst_pin = Pin(rst, Pin.OUT, value=1)
        self.addr = addr
        self.freq = freq
        self.lcd = I2C(self.id, sda=self.sda_pin, scl=self.scl_pin, freq=self.freq)
        time.sleep_ms(50)
        self.lcd.writeto(self.addr, b'\x00\x39\x14\x78\x5e\x6d\x0f\x01\x06')
        time.sleep_ms(2)
    
    #set screen contrast
    def setContrast(self, contrast=8):
        if 2 <= contrast and contrast <= 15:
            content = (0x70 + contrast).to_bytes(1, 'big')
            self.lcd.writeto(self.addr, b'\x00\x39' + content)
    
    #set cursor position
    def cursorPos(self, row=0, pos=0):
        if (row == 0 or row == 1) and (0 <= pos and pos <= 19):
            self.lcd.writeto(self.addr, b'\x00' + self.getByte(0x80 + 0x40 * row + pos))
    
    #resets associated lcd
    def reset(self):
        self.rst_pin.value(0)
        self.rst_pin.value(1)
    
    #sends 'clear screen' command
    def clear(self):
        self.lcd.writeto(self.addr, b'\x00\x01')
    
    #writes out the specified string to the specified line, does not clear screen before writing
    def line_out(self, msg, line=0):
        self.lcd.writeto(self.addr, b'\x80' + (line != 1) * b'\x80\x40' + (line == 1) * b'\xc0\x40' + bytes(msg, 'ascii'))
    
    #writes out the specified string array, clears screen before writing
    def output(self, msg):
        self.lcd.writeto(self.addr, b'\x00\x01')
        time.sleep_ms(1)
        self.lcd.writeto(self.addr, b'\x80\x80\x40' + bytes(msg[0], 'ascii'))
        self.lcd.writeto(self.addr, b'\x80\xc0\x40' + bytes(msg[1], 'ascii'))
    
    #create byte of desired value
    def getByte(self, value):
        if 0 <= int(value) and int(value) <= 255:
            return value.to_bytes(1, 'big')
        else:
            return b'\x00'
    
    #appends a character specified by hex
    def chAppend(self, char):
        self.lcd.writeto(self.addr, b'\x40' + self.getByte(char))
    
    #dev function for sending raw bytes to the lcd
    def sendBytes(self, content):
        self.lcd.writeto(self.addr, content)



#### FUNCTION DEFS ####
#shifting cursor char, direct = 1 -> right shift, direct = -1 -> left shift
def shiftCursor(msg, direct):
    global cursorPos
    #ensure valid direct value
    if direct != 1 and direct != -1:
        return msg
    temp = list(msg)
    max_index = len(temp)-1
    perms = promptPerms[promptIndex]
    #either no blanks or left/right always advance
    if perms[3] != "y":
        msg = changePrompt(msg, direct)
        return msg
    #goto last prompt
    if (cursorPos == 0 and direct == -1):
        msg = changePrompt(msg, -1)
        return msg
    if temp[cursorPos + direct].isdigit():
        cursorPos += direct
        return msg
    if perms[0] == "y" or (temp[cursorPos + direct] != '.' and (not temp[cursorPos + direct].isdigit())):
        msg = changePrompt(msg, 1)
        return msg
    #handle the special case with .'s, ensure next char is a digit
    if temp[cursorPos + direct] == '.' and temp[cursorPos + 2 * direct].isdigit():
        cursorPos += 2 * direct
    return msg

#increment number pointed to by cursor
#output is mod 10 so no matter the signed-ness or size of inc,
#char output range is 0-9, or 1-4 for solenoid count input
def incrPointedNum(msg, inc):
    temp = list(msg)
    perms = promptPerms[promptIndex]
    if perms[1] == "y":
        msg = changePrompt(msg, 1)
        return msg
    #increment pointed char if possible
    minChar = (perms[4] == "s") * ord('1') + (perms[4] != "s") * ord('0') #if on solenoid count, input may
    maxChar = (perms[4] == "s") * ord('4') + (perms[4] != "s") * ord('9') #range from 1-4, else okay range is from 0-9
    if temp[cursorPos].isdigit():
        temp[cursorPos] = chr((ord(temp[cursorPos]) + inc - minChar) % (maxChar - minChar + 1) + minChar)
        msg = ''.join(temp)
    return msg


#fetch and store the current data on the prompt (prep for prompt change)
def savePromptData(msg):
    global numSol, channelData
    perms = promptPerms[promptIndex]
    #no data to save case
    if perms[3] != "y":
        return 0
    #syntax for substrings: variable[beginning : beginning + length]
    if perms[5] == "p":
        temp = msg[0:2]
    else:
        temp = msg[0:4]
    
    if perms[5] == "i" or perms[5] == "p":
        outp = int(temp)
    elif perms[5] == "f":
        x = float(temp)
        outp = (x <= 2) * 2 + (2 < x and x < 40) * x + (x >= 40) * 40
    else:
        outp = 0
    #save the data
    if perms[4] == "s":
        numSol = outp
    else:
        clamped = int(perms[4])
        clamped = (0 < clamped and clamped < 5) * clamped + (clamped >= 5) * 5
        channelData[clamped] = outp

#handle the prompt adjustment when the user gives
#a prompt change notice by trying to move the cursor off the screen
def changePrompt(msg, inc):
    global promptIndex,channelIndex,channelData,disp_text,infoEntered,updated,firstTime,channelPhases,cycleCount,cursorPos,allData
    newData = []
    #catch bad combos/values
    if (inc != 1 and inc != -1) or promptIndex < 0 or promptIndex > maxPromptIndex:
        return msg
    savePromptData(msg)
    updated = True
    #handle updating promptIndex given perms
    perms = promptPerms[promptIndex]
    if perms[0] == "y":
        promptIndex += 1
    elif perms[2] == "c":
        saveToDB(channelIndex, channelData)
        if inc == 1 and (channelIndex + 1) != numSol:
            #more solenoid channel info to enter, so let's do that
            promptIndex = 2
            channelIndex += 1
            channelData = readFromDB(channelIndex)
        else:
            promptIndex += inc
    elif perms[2] == "r":
        if inc == 1:
            promptIndex += 1
            lcd.clear()
        else:
            #return to first prompt from running phase
            promptIndex = 1
            channelIndex = 0
            channelData = readFromDB(channelIndex)
            infoEntered = False
            firstTime = True
            #### CHANNEL RESET ####
            slnd0.duty_u16(0)
            slnd1.duty_u16(0)
            slnd2.duty_u16(0)
            slnd3.duty_u16(0)
            channelPhases = [0,0,0,0]
            cycleCount = [1,1,1,1]
    else:
        promptIndex += inc
    
    #On final prompt, everything's in and start outputting
    if promptIndex == (maxPromptIndex - 1):
        infoEntered = True
        allData[0] = readFromDB(0)
        allData[1] = readFromDB(1)
        allData[2] = readFromDB(2)
        allData[3] = readFromDB(3)
    #fill in prompt blanks (newData)
    if promptIndex != maxPromptIndex:
        perms = promptPerms[promptIndex] #get perms of new prompt
        if perms[3] == "y":
            if perms[4] == "s":
                newData = [numSol]
            else:
                clamped = int(perms[4])
                clamped = (0 < clamped and clamped < 5) * clamped + (clamped >= 5) * 5
                newData = [channelData[clamped], channelIndex+1]
            cursorPos = 0
        else:
            cursorPos = 19
    #update screen if possible
    if promptIndex < maxPromptIndex:
        disp_text[0] = prompts[2*promptIndex]
        msg = prompts[2*promptIndex+1].format(*newData)
    return msg




