import RPi.GPIO as GPIO
import time

led = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

for i in range(4):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(led, GPIO.LOW)
    time.sleep(0.2)

GPIO.cleanup()
