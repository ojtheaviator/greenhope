import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI

import time                            #calling time to provide delays in program

IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(13,IO.OUT)           # initialize GPIO19 as an output.

p = IO.PWM(13,25000)          #GPIO19 as PWM output, with 100Hz frequency

p.start(0)                              #generate PWM signal with 0% duty cycle

try:
    while True:                               #execute loop forever
        for x in [0,33, 67, 100, 67, 33]:
            print(f"Duty cycle: {x}%")
            p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
            time.sleep(3)                           #sleep for 100m second
            

except KeyboardInterrupt:
    IO.cleanup()
    print("\nDone!\n")
