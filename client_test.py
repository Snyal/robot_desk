import threading
import speech_recognition as sr
from robots.robot_c import Robot_Client


thread_cond = threading.Condition()
id_action = 0 
       
print("Starting Robot")
#robot_local = Robot_Client()
robot_local = Robot_Client(90,0)

print(robot_local.get_humans_information(0))
