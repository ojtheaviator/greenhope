import RPi.GPIO as GPIO
import time

#led = [29, 31, 33][int(input("0, 1, or 2?: "))]
#led = [29, 31][int(input("0 or 1?: "))]

#light is 29


GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

'''
for i in range(2):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(10)
    GPIO.output(led, GPIO.LOW)
    time.sleep(10)


GPIO.output(led, GPIO.HIGH)
input("enter to continue")
GPIO.output(led, GPIO.LOW)
'''

GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)
input("enter to continue")
GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)


GPIO.cleanup()
