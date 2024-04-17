import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)



GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)


GPIO.output(29, GPIO.LOW)
GPIO.output(31, GPIO.LOW)



GPIO.cleanup()
