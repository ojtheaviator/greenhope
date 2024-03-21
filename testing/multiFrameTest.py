import can
import math

# Function to split the bytestring into 8-byte chunks
def split_bytestring(bytestring, chunk_size=8):
    # Calculate the number of chunks needed
    n_chunks = math.ceil(len(bytestring) / chunk_size)
    # Split the bytestring into chunks
    return [bytestring[i * chunk_size:(i + 1) * chunk_size] for i in range(n_chunks)]

# Function to send a bytestring over CAN
def send_bytestring(bus, bytestring, arbitration_id=0x123):
    chunks = split_bytestring(bytestring)
    for chunk in chunks:
        message = can.Message(arbitration_id=arbitration_id, data=chunk, is_extended_id=False)
        bus.send(message)
        print(f"Sent: {chunk.hex()}")

# Function to receive bytestrings over CAN
def receive_bytestring(bus, expected_chunks):
    chunks = []
    while len(chunks) < expected_chunks:
        message = bus.recv()  # Block until a message is received
        chunks.append(message.data)
        print(f"Received: {message.data.hex()}")
    return b''.join(chunks)

# Example usage
if __name__ == "__main__":
    # Replace 'your_channel_here' with your actual CAN channel
    bus = can.interface.Bus(bustype='socketcan', channel='your_channel_here', bitrate=500000)
    
    # Example bytestring to send
    original_bytestring = b'\x01' * 36  # An example bytestring longer than 8 bytes
    
    # Send the bytestring
    send_bytestring(bus, original_bytestring)
    
    # Assuming the sender and receiver are different scripts or run sequentially
    # Calculate the number of expected chunks
    expected_chunks = math.ceil(len(original_bytestring) / 8)
    
    # Receive the bytestring
    received_bytestring = receive_bytestring(bus, expected_chunks)
    print(f"Complete received bytestring: {received_bytestring.hex()}")
