import RPi.GPIO as GPIO
import time

led = [29, 31, 33][int(input("0, 1, or 2?: "))]

#light is 29


GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

'''
for i in range(2):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(led, GPIO.LOW)
    time.sleep(10)
'''

GPIO.output(led, GPIO.HIGH)
input("enter to continue")
GPIO.output(led, GPIO.LOW)

GPIO.cleanup()
