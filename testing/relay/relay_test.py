import RPi.GPIO as GPIO
import time

#led = [29, 31, 33][int(input("0, 1, or 2?: "))]
#led = [29, 31][int(input("0 or 1?: "))]
led = [29, 31, 33, 11, 13][int(input("0, 1, 2, 3, or 4?: "))]

#light is 29 on hub
#pump is 33 on hub
#heater is 31 on hub
#ph acid is 11 on hub
#ph base is 13 on hub


GPIO.setmode(GPIO.BOARD)

GPIO.setup(led, GPIO.OUT)



'''
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)



for i in range(1):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(led, GPIO.LOW)
    time.sleep(10)

    time.sleep(1)
'''


GPIO.output(led, GPIO.HIGH)
input("enter to continue")
GPIO.output(led, GPIO.LOW)
'''
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)
input("enter to continue")
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)
'''


GPIO.cleanup()
