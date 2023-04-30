import json
import socket
import cv2
import pickle
import struct
import numpy as np
from robots.robot_s import Robot_Server
from utils import init_cam_distortion, take_picture, undistort 

# init server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345                             # Reserve a port for your service.
s.bind(("192.168.155.180", port))                     # Bind to the port
s.listen(1)

print('Socket now listening')

conn_client,addr=s.accept()
payload_size = struct.calcsize(">LI")

# Robot init
robot = Robot_Server()

# Camera init
K,D,DIM = init_cam_distortion()

# main loop server
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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = undistort(frame, K, D, DIM)
    
    # store last frame
    robot.add_frame(frame)

    # start action robot:
    
    if action == 5:
        take_picture(robot)
    
    robot.change_state(action)
    detection_result_image, boundingsBox = robot.make_action()
    detection_result_image = cv2.resize(detection_result_image, (960,540), interpolation= cv2.INTER_LINEAR)

    data = json.dumps({"boudingBox": boundingsBox, "action": action})
    conn_client.send(data.encode())

    cv2.imshow('ImageWindow',detection_result_image)
    cv2.waitKey(1)