import can
import math

# Function to split the bitstring into chunks of 64 bits (8 bytes)
def split_bitstring(bitstring, chunk_size=64):
    # Calculate the number of chunks needed
    n_chunks = math.ceil(len(bitstring) / chunk_size)
    # Split the bitstring into chunks
    return [bitstring[i * chunk_size:(i + 1) * chunk_size] for i in range(n_chunks)]

# Function to combine chunks of bitstring back into a single bitstring
def combine_bitstrings(chunks):
    return ''.join(chunks)

# Function to send a bitstring over CAN
def send_bitstring(bus, bitstring, arbitration_id=0x123):
    chunks = split_bitstring(bitstring)
    for chunk in chunks:
        # Convert the bitstring chunk to bytes
        data = int(chunk, 2).to_bytes(len(chunk) // 8, byteorder='big')
        message = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
        bus.send(message)
        print(f"Sent: {data.hex()}")

# Function to receive bitstrings over CAN
def receive_bitstring(bus, expected_chunks):
    chunks = []
    while len(chunks) < expected_chunks:
        message = bus.recv()  # Block until a message is received
        chunk = bin(int.from_bytes(message.data, byteorder='big'))[2:].zfill(8 * len(message.data))
        chunks.append(chunk)
        print(f"Received: {chunk}")
    return combine_bitstrings(chunks)

# Example usage
if __name__ == "__main__":
    # Replace 'your_channel_here' with your actual CAN channel
    bus = can.interface.Bus(bustype='socketcan', channel='your_channel_here', bitrate=500000)
    
    # Example bitstring to send
    original_bitstring = '1' * 500  # An example bitstring longer than 64 bits
    
    # Send the bitstring
    send_bitstring(bus, original_bitstring)
    
    # Assuming the sender and receiver are different scripts or run sequentially
    # Calculate the number of expected chunks
    expected_chunks = math.ceil(len(original_bitstring) / 64)
    
    # Receive the bitstring
    received_bitstring = receive_bitstring(bus, expected_chunks)
    print(f"Complete received bitstring: {received_bitstring}")

