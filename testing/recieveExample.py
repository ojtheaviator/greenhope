import can
import pickle

def receive_can_message(channel='can0', message_id=0x123):
    bus = can.interface.Bus(channel=channel, bustype='socketcan', fd=True)
    
    while True:
        message = bus.recv()  # Block until a message is received
        if message.arbitration_id == message_id:
            try:
                # Deserialize the data back into a Python object
                obj = pickle.loads(message.data)
                print(f"Received object: {obj}")
            except (pickle.PickleError, EOFError):
                print("Could not deserialize the received data.")

if __name__ == "__main__":
    receive_can_message()
