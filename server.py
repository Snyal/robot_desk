import socket
import cv2
import pickle
import struct

from robots.robot_s import Robot_Server 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345                             # Reserve a port for your service.
s.bind(("192.168.171.180", port))                     # Bind to the port
s.listen(1)

print('Socket now listening')

conn_client,addr=s.accept()
payload_size = struct.calcsize(">LI")

# Robot init
robot = Robot_Server()

while True:  
    data = conn_client.recv(100)
    
    packed_msg = data[:payload_size]
    data = data[payload_size:]

    msg_data = struct.unpack(">LI", packed_msg)
    msg_size = msg_data[0]
    action = msg_data[1]

    while len(data) < msg_size:
        data += conn_client.recv(100)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    # store last frame
    robot.add_frame(frame)

    # start action robot:
    robot.change_state(action)
    detection_result_image = robot.make_action()
    conn_client.send("Done".encode())

    cv2.imshow('ImageWindow',detection_result_image)
    cv2.waitKey(1)