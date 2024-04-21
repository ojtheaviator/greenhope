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
        print("CAN: initializing")
        # initializing instance variable
        self.my_id = my_id
        self.bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
    
    def close(self):
        print("CAN: closing")
        self.bus.shutdown()
    
    def __del__(self):
        print("CAN: shutting down")
        self.bus.shutdown()

    # Function to split the bytestring into 8-byte chunks
    def split_bytestring(self, bytestring, chunk_size=8):
        # Calculate the number of chunks needed
        n_chunks = math.ceil(len(bytestring) / chunk_size)
        # Split the bytestring into chunks
        return [bytestring[i * chunk_size:(i + 1) * chunk_size] for i in range(n_chunks)]

    # Function to send a bytestring over CAN
    def send_bytestring(self, bytestring, arbitration_id=0x000, message_id=0):
        message_id = message_id%64
        print("CAN: sending bytestring")
        chunks = self.split_bytestring(bytestring, 7)  # Payload size reduced to 7
        num_chunks = len(chunks)
        try:
            for i, chunk in enumerate(chunks):
                # Prepare the flag byte
                if i == 0:
                    flag = 0x00  # Start chunk
                elif i == num_chunks - 1:
                    flag = 0xC0  # End chunk
                else:
                    flag = 0x40  # Middle chunk

                # Apply message ID within the flag byte
                flag |= message_id & 0x3F

                # Append flag byte to chunk
                full_chunk = chunk + bytes([flag])

                message = can.Message(arbitration_id=arbitration_id, data=full_chunk, is_extended_id=False)
                self.bus.send(message)
            print("CAN: bytestring sent")
        except can.CanOperationError as e:
            print(e)

    # Improved receive function
    def receive_my_id(self, timeout=None):
        while True:
            message = self.bus.recv(timeout)
            if message and (message.arbitration_id == self.my_id):
                return(message)

    # Function to receive bytestrings over CAN
    async def receive_bytestring(self, timeout=1):
        loop = asyncio.get_event_loop()
        chunks = []
        current_message_id = None

        with concurrent.futures.ThreadPoolExecutor() as pool:
            while True:
                message = await loop.run_in_executor(pool, lambda: self.receive_my_id(timeout))
                if not message:
                    raise ValueError('Incomplete CAN message')

                data = message.data[:-1]  # Payload
                flag_byte = message.data[-1]
                msg_id = flag_byte & 0x3F
                msg_type = flag_byte & 0xC0

                if msg_type == 0x00:  # Start chunk
                    chunks = [data]
                    current_message_id = msg_id
                elif msg_id == current_message_id:
                    if msg_type == 0xC0:  # End chunk
                        chunks.append(data)
                        break
                    elif msg_type == 0x40:  # Middle chunk
                        chunks.append(data)
                    else:
                        raise ValueError(f'Received chunk with unexpected flags or mismatched message ID. Flag: {flag_byte:#04x}, Expected ID: {current_message_id}, Received ID: {msg_id}')

        return b''.join(chunks)


    def transmit(self, payload, message_id=0x000, new_id=0):
        original_bytestring = pickle.dumps(payload)
        self.send_bytestring(original_bytestring, message_id, new_id)

    async def receive(self):
        while True:
            try:
                print("CAN: listening for message...")
                received_bytestring = await self.receive_bytestring()
                print("CAN: message recieved, decoding")
                return(pickle.loads(received_bytestring))
            except ValueError as e:
                print(f"\nWARN: {e}\n")
            except pickle.UnpicklingError:
                print("\nWARN: Huh, weird, unpickling error but no timeout. At any rate, we're waiting for next message now\n")
