import json
import socket
import struct
import threading
import time
import cv2
import pickle
import speech_recognition as sr
from robots.robot_c import Robot_Client
from robots.utils.microphone import Microphone

thread_cond = threading.Condition()
id_action = 0 

def cam_task():

    global id_action # make global variable
    try:
        while True:
            # get locker
            _, frame = cam.read()

            # transform image to bytes
            _, frame = cv2.imencode('.jpg', frame, encode_param)

            data = pickle.dumps(frame, id_action)
            size = len(data)
            
            # send image to server
            client_socket.sendall(struct.pack(">LI", size, id_action) + data)

            if id_action == 5:
                id_action = 0

            dataFromServer = client_socket.recv(1024)
            dataFromServer = json.loads(dataFromServer.decode())

            print(dataFromServer)


    except:
        print("Camera doesn't work!")

def micro_task(source):

    global id_action # make global variable
    
    #INIT
    microphone = Microphone()

    try:
        while True:
                # listen microphonediesel  
                command = ""

                if microphone.is_activate:              
                    voice = key_word_listener.listen(source, phrase_time_limit=2)  
                else : 
                    continue

                try :
                    command = key_word_listener.recognize_google(voice, language="fr-FR")
                except:
                    print("no keyworkd")
                    
                if 'Alexa' in command or 'alexa' in command:
                    try :
                        # rotate head robot to user
                        #angle_x = microphone.get_orientation_last_ear()
                        #robot_local.head_Robot.rotate_head(angle_x = angle_x, angle_y = robot_local.head_Robot.current_y_angle)

                        print('listening...')
                        voice = phrases_listener.listen(source)
                        command = phrases_listener.recognize_google(voice, language="fr-FR")
                                                                
                        # init question
                        robot_local.question = command
                        #print("make action ...")
                        answer, id_action = robot_local.make_action_question()   
                        print(answer)
                            
                    except :
                        print("error")

                if 'arrêter' in command:
                    print("stop...")
                    break
    except:
        print("Microphone doesn't work!")    

def picture_task():

    global id_action

    while True :
        time.sleep(3)
        print("photo")
        id_action = 5

print("Starting Robot...")
#robot_local = Robot_Client()                    
robot_local = Robot_Client(90,30)

# init client socket
try:
    host = socket.gethostname()             
    port = 12345                           

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.155.180", port))
    #connection = client_socket.makefile('wb')
except:
    "server not found"

robot_local.head_Robot.rotate_head(angle_x = 90, angle_y=30)

# camera
print("Robot is ready")
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
cam_thread = threading.Thread(target=cam_task)
cam_thread.start()

cap = cv2.VideoCapture(0) # this is the magic!


#microphone 
key_word_listener = sr.Recognizer()
phrases_listener = sr.Recognizer()
with sr.Microphone() as source:
    micro_thread = threading.Thread(target=micro_task(source))
    micro_thread.start()

#picture_thread = threading.Thread(target=picture_task())
#picture_thread.start()

cam_thread.join()
micro_thread.join()
#picture_thread.join()
