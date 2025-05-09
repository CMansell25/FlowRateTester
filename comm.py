##Data is a wrapper
##

from sys import stdin, exit
from _thread import start_new_thread
import time
import isr



class Data:
    def __init__(self) -> None:
        pass


class Buffer:
    def __init__(self) -> None:
        self.bufferSize = 1024
        self.buffer = [' ']* self.bufferSize
        self.bufferNextIn = 0
        self.bufferNextOut = 0
        self.bufferEcho = True
        self.terminateThread = False

    

    def fillBuffer(self):
        self.pull()
        while True:
            if self.terminateThread:
                break
            self.buffer[self.bufferNextIn] = stdin.read(1)
            if self.bufferEcho:
                print(self.buffer[self.bufferNextIn], end='')
            self.bufferNextIn +=1
            if self.bufferNextIn == self.bufferSize:
                self.bufferNextIn = 0
        



    def getLineBuffer(self):

        if self.bufferNextOut == self.bufferNextIn:
            return ''
        
        n = self.bufferNextOut
        while self.bufferNextIn != n :
            if self.buffer[n] == '\x0a':
                break
            n +=1
            if n == self.bufferSize:
                n = 0
        if n == self.bufferNextIn:
            return ''
        
        line = ''
        n +=1
        if n == self.bufferSize:
            n = 0
        
        while self.bufferNextOut != n:

            if self.buffer[self.bufferNextOut] == '\x0d':
                self.bufferNextOut += 1
                if self.bufferNextOut == self.bufferSize:
                    self.bufferNextOut = 0
                continue

            if self.buffer[self.bufferNextOut] == '\x0a':
                self.bufferNextOut += 1
                if self.bufferNextOut == self.bufferSize:
                    self.bufferNextOut = 0
                break
            line = line + self.buffer[self.bufferNextOut]
            self.bufferNextOut += 1
            if self.bufferNextOut == self.bufferSize:
                self.bufferNextOut = 0
        return line


    def pull(self):
 
        try:
            while True:
                buffLine = self.getLineBuffer()
                if buffLine:
                    print (buffLine)


                time.sleep(0.1)
        except KeyboardInterrupt:
            self.terminateThread = True
            exit()
        except isr.backIH.interrupt_flag:
            self.terminateThread = True








