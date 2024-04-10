import asyncio
import random
from sillylib import silly

class Can:
    # constructor
    def __init__(self):
        # initializing instance variable
        self.num=100

    # a method
    def transmit(self, payload):
        print(f"CAN message fake transmitted: {payload}")

    def recieve(self, payload):
        while True:
            #await asyncio.sleep(0.001)
            if (random.random() < 0.001):
                print(f"fake CAN message recieved{silly()}")
