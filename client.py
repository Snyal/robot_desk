from locale import atoi
import socket
import struct
import threading
import time
import cv2
import pickle
import speech_recognition as sr
from robots.robot_c import Robot_Client


thread_cond = threading.Condition()
id_action = 0 

def cam_task():

    global id_action # make global variable
    id_action = 1
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
            dataFromServer = client_socket.recv(1024)
    except:
        print("Camera doesn't work!")

def micro_task(source):

    global id_action # make global variable
    
    robot_local.head_Robot.rotate_head(angle_x = 90, angle_y=90)
    try:
        while True:
                print('listening...')
                # listen microphone
                voice = listener.listen(source)
       
                try :
                    
                    command = listener.recognize_google(voice, language="fr-FR")
                    # check if starter word was in the command
                
                    if 'diesel' in command:
      
                        command = command.replace('diesel ', '')

                        # init question
                        robot_local.question = command

                        if "droite" in command :
                            print("COMMANDE DROITE")
                            robot_local.head_Robot.rotate_head(angle_x = 180, angle_y = robot_local.head_Robot.current_y_angle)
                        
                        if "gauche" in command :
                            print("COMMANDE GAUCHE")
                            robot_local.head_Robot.rotate_head(angle_x = 0, angle_y = robot_local.head_Robot.current_y_angle)
                        
                        if "milieu" in command :
                            print("COMMANDE MILIEU")
                            robot_local.head_Robot.rotate_head(angle_x = 90, angle_y = 90)
                        
                        if "haut" in command :
                            print("COMMANDE HAUT")
                            robot_local.head_Robot.rotate_head(angle_x = robot_local.head_Robot.current_x_angle, angle_y = 0)

                        if "bas" in command :
                            print("COMMANDE BAS")
                            robot_local.head_Robot.rotate_head(angle_x = robot_local.head_Robot.current_x_angle, angle_y = 180)

                        # process question to robot
                        
                        # TODO : process pre-answered questions
                        #answer = robot_local.make_action_question()   
                        #print(answer)

                        # TODO : replace by pre-answered questions
                        id_action += 1
                        id_action %= 2

                        #print("je change id_action",id_action)

                        
                except :
                    command = command.lower()
                #thread_cond.release()

    except:
        print("Microphone doesn't work!")    
                
    
def head_task():
    counter = 0
    while True : 
        robot_local.head_Robot.rotate_head(angle_x = counter%180, angle_y= 0)
        counter+=5
       
print("Starting Robot")
robot_local = Robot_Client()
#robot_local = Robot_Client(90,0)

# init client socket
try:
    host = socket.gethostname()             
    port = 12345                           

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.87.180", port))
    connection = client_socket.makefile('wb')
except:
    "server not found"

cam = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

print("Robot is ready")
cam_thread = threading.Thread(target=cam_task)
cam_thread.start()

listener = sr.Recognizer()
with sr.Microphone() as source:
    micro_thread = threading.Thread(target=micro_task(source))
    micro_thread.start()

#TEMPO
# head_thread = threading.Thread(target=head_task)
# head_thread.start()

cam_thread.join()
micro_thread.join()
#head_thread.join()