#Both hub and module!

import RPi.GPIO as GPIO
import asyncio

class Hub:
    def __init__(self):
        self.phpPin = 5 #29
        self.phmPin = 6 #31
        self.heatPin = 13 #33
        self.lightPin = 17 #11
        self.pumpPin = 27 #13
        
#        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.phpPin, GPIO.OUT)
        GPIO.setup(self.phmPin, GPIO.OUT)
        GPIO.setup(self.heatPin, GPIO.OUT)
        GPIO.setup(self.lightPin, GPIO.OUT)
        GPIO.setup(self.pumpPin, GPIO.OUT)
        
    
    def __del__(self):
        GPIO.cleanup()
    
    def close(self):
        GPIO.cleanup()
    
    async def phUp(self, pumptime=0.2):
        GPIO.output(self.phpPin, GPIO.HIGH)
        await asyncio.sleep(pumptime)
        GPIO.output(self.phpPin, GPIO.LOW)
    
    async def phDown(self, pumptime=0.2):
        GPIO.output(self.phmPin, GPIO.HIGH)
        await asyncio.sleep(pumptime)
        GPIO.output(self.phmPin, GPIO.LOW)
    
    def lightsOn(self, shouldBeOn):
        if shouldBeOn:
            GPIO.output(self.lightPin, GPIO.HIGH)
        else:
            GPIO.output(self.lightPin, GPIO.LOW)
    
    def pumpOn(self, shouldBeOn):
        if shouldBeOn:
            GPIO.output(self.pumpPin, GPIO.HIGH)
        else:
            GPIO.output(self.pumpPin, GPIO.LOW)
    
    def heatOn(self, shouldBeOn):
        if shouldBeOn:
            GPIO.output(self.heatPin, GPIO.HIGH)
        else:
            GPIO.output(self.heatPin, GPIO.LOW)
            

class Module:
    def __init__(self, initialDutyCycle=100):
        self.heataPin = 5 #29
        self.heatbPin = 6 #31
        self.fanPin = 13 #33
        
#        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.heataPin, GPIO.OUT)
        GPIO.setup(self.heatbPin, GPIO.OUT)
        GPIO.setup(self.fanPin, GPIO.OUT)
        
        self.fan = GPIO.PWM(self.fanPin, 25000)
        self.fan.start(initialDutyCycle)
        
        self.heataOn(False)
        self.heatbOn(False)

    def __del__(self):
        GPIO.cleanup()
    
    def close(self):
        GPIO.cleanup()
    
    def heataOn(self, shouldBeOn):
        if shouldBeOn:
            GPIO.output(self.heataPin, GPIO.HIGH)
        else:
            GPIO.output(self.heataPin, GPIO.LOW)
    
    def heatbOn(self, shouldBeOn):
        if shouldBeOn:
            GPIO.output(self.heatbPin, GPIO.HIGH)
        else:
            GPIO.output(self.heatbPin, GPIO.LOW)
    
    def setFan(self, dutyPercent):
        self.fan.ChangeDutyCycle(dutyPercent)
