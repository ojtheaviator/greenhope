import can
import pickle
import time

def send_can_message(channel='can0', message_id=0x123, obj=None):
    bus = can.interface.Bus(channel=channel, bustype='socketcan', fd=True)
    
    # Serialize the object to bytes
    serialized_obj = pickle.dumps(obj)
    
    # For simplicity, we assume the serialized object fits in one CAN FD frame
    msg = can.Message(arbitration_id=message_id,
                      data=serialized_obj,
                      is_extended_id=False,
                      is_fd=True)
    
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message failed to send")

if __name__ == "__main__":
    obj_to_send = {'key': 'value', 'number': 42}  # Example Python object
    while True:
        send_can_message(obj=obj_to_send)
        time.sleep(1)
