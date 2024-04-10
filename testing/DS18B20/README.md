To enable 1-wire, edit /boot/config.txt with:

if "dtoverlay=w1-gpio" is there, add ",gpiopin=23" to that line
otherwise add "dtoverlay=w1-gpio,gpiopin=23" to the file
