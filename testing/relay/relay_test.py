import RPi.GPIO as GPIO
import time

led = [29, 31, 33, 11, 13][int(input("0, 1, 2, 3, or 4?: "))]

#light is 29 on hub
#pump is 33 on hub
#heater is 31 on hub
#ph acid is 11 on hub
#ph base is 13 on hub


GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

'''
for i in range(1):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)
    time.sleep(1)

'''

GPIO.output(led, GPIO.HIGH)
input("enter to continue")
GPIO.output(led, GPIO.LOW)


GPIO.cleanup()
