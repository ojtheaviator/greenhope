import can
import math
import pickle
import time

# Improved integer input function
def inputInt(message, intRange = []):
    if (len(intRange) != 0) and (len(intRange) != 2):
        raise ValueError('The given integer range is invalid (it should either be left blank for any integer or [a, b] for a specific range)')
    while True:
        try:
            out = int(input(message))
            if (len(intRange) == 2) and ((out < intRange[0]) or (out > intRange[1])):
                print(f"Input out of bounds [{intRange[0]}, {intRange[1]}]")
            else:
                return(out)
        except ValueError:
            print("Invalid input. Please try again!")


# Function to split the bytestring into 8-byte chunks
def split_bytestring(bytestring, chunk_size=8):
    # Calculate the number of chunks needed
    n_chunks = math.ceil(len(bytestring) / chunk_size)
    # Split the bytestring into chunks
    return [bytestring[i * chunk_size:(i + 1) * chunk_size] for i in range(n_chunks)]

# Function to send a bytestring over CAN
def send_bytestring(bus, bytestring, arbitration_id=0x000):
    chunks = split_bytestring(bytestring)
    
    lengthBytes = len(chunks).to_bytes(8, "big")
    print(f"Sending {len(chunks)*8} Bytes now")
    message = can.Message(arbitration_id=arbitration_id, data=lengthBytes, is_extended_id=False)
    bus.send(message)

    for chunk in chunks:
        message = can.Message(arbitration_id=arbitration_id, data=chunk, is_extended_id=False)
        bus.send(message)
        #print(f"Sent: {chunk.hex()}")

# Improved receive function
def receive_my_id(bus, message_id=0x000, timeout=None):
    while True:
        message = bus.recv(timeout)
        if (message.arbitration_id == message_id):
            return(message)

# Function to receive bytestrings over CAN
def receive_bytestring(bus):
    chunks = []
    
    expected_chunks_bytes = receive_my_id(bus)
    expected_chunks = int.from_bytes(expected_chunks_bytes, "big")

    while len(chunks) < expected_chunks:
        message = receive_my_id(bus, timeout = 1)  # Block until a message is received
        chunks.append(message.data)
        #print(f"Received: {message.data.hex()}")
    return b''.join(chunks)


def sendObject(bus, sendObject, message_id=0x000):
    original_bytestring = pickle.dumps(sendObject)
    send_bytestring(bus, original_bytestring, message_id)

def receiveObject(bus, our_id=0x000):
    received_bytestring = receive_bytestring(bus)
    return(pickle.loads(received_bytestring))
    
    
# Example usage
if __name__ == "__main__":
    sendOrReceive = inputInt("Please choose one of the options:\n0: Send\n1: Receive\n", [0, 1])    

    sendData = ""
    if sendOrReceive == 0:
        sendData = input("Enter text to send or leave blank to send default test: ")
        if sendData == "":
            filename = input("Enter filename of text file to send: ")
            if filename == "":
                sendData = ["test stuff", 3.1415, ["cats", "bananas", -100.5]]
            else:
                with open(filename, "r") as fid:
                    sendData = fid.read()
                
    with can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000) as bus:
        
        if sendOrReceive == 0:
            t1 = time.time()
            sendObject(bus, sendData)
            print(f"Time to send: {time.time() - t1} s")
        else:
            # Receive the bytestring
            received_data = receiveObject(bus)
            print(f"Complete received object: {received_data}")
