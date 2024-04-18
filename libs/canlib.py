#Both hub and module!

import asyncio
import concurrent.futures
import can
import math
import pickle
import time

class Can:
    # constructor
    def __init__(self, my_id):
        # initializing instance variable
        self.my_id = my_id
        self.bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
    
    def close(self):
        self.bus.shutdown()
    
    def __del__(self):
        self.bus.shutdown()

    # Function to split the bytestring into 8-byte chunks
    def split_bytestring(self, bytestring, chunk_size=8):
        # Calculate the number of chunks needed
        n_chunks = math.ceil(len(bytestring) / chunk_size)
        # Split the bytestring into chunks
        return [bytestring[i * chunk_size:(i + 1) * chunk_size] for i in range(n_chunks)]

    # Function to send a bytestring over CAN
    def send_bytestring(self, bytestring, arbitration_id=0x000):
        chunks = self.split_bytestring(bytestring)
        
        lengthBytes = len(chunks).to_bytes(8, "big")
        #print(f"Sending {len(chunks)*8} Bytes now")
        message = can.Message(arbitration_id=arbitration_id, data=lengthBytes, is_extended_id=False)
        try:
            self.bus.send(message)
            for chunk in chunks:
                message = can.Message(arbitration_id=arbitration_id, data=chunk, is_extended_id=False)
                self.bus.send(message)
        except can.CanOperationError as e:
            print(e)

    # Improved receive function
    def receive_my_id(self, timeout=None):
        while True:
            message = self.bus.recv(timeout)
            if message and (message.arbitration_id == self.my_id):
                return(message)

    # Function to receive bytestrings over CAN
    async def receive_bytestring(self):
        loop = asyncio.get_event_loop()
        first_message = await loop.run_in_executor(None, self.receive_my_id)
        expected_chunks = int.from_bytes(first_message.data, "big")
        chunks = []

        with concurrent.futures.ThreadPoolExecutor() as pool:
            while len(chunks) < expected_chunks:
                message = await loop.run_in_executor(pool, self.receive_my_id)
                chunks.append(message.data)

        return b''.join(chunks)


    def transmit(self, payload, message_id=0x000):
        original_bytestring = pickle.dumps(payload)
        self.send_bytestring(original_bytestring, message_id)

    def receive(self):
        received_bytestring = self.receive_bytestring()
        return(pickle.loads(received_bytestring))
