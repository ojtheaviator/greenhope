import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time


# create the spi bus
spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.CE0)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

pin = int(input("Enter pin num (0-7): "))
exec(f"mcppin=MCP.P{pin}")

# create an analog input channel on pin 0
chan = AnalogIn(mcp, mcppin)

try:
    while True:
        print("Raw ADC Value: ", chan.value)
        print("ADC Voltage: " + str(chan.voltage) + "V")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDone!")
