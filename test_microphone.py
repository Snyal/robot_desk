import threading
import speech_recognition as sr
from robots.robot_c import Robot_Client
from robots.utils.microphone import Microphone

thread_cond = threading.Condition()
id_action = 0 

def micro_task(source):

    global id_action # make global variable
    
    #INIT
    robot_local.head_Robot.rotate_head(angle_x = 90, angle_y=90)
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
                    
                if 'écoute' in command:
                    try :
                        # rotate head robot to user
                        angle_x = microphone.get_orientation_last_ear()
                        robot_local.head_Robot.rotate_head(angle_x = angle_x, angle_y = robot_local.head_Robot.current_y_angle)

                        print('listening...')
                        voice = phrases_listener.listen(source)
                        command = phrases_listener.recognize_google(voice, language="fr-FR")
                                                                
                        # init question
                        robot_local.question = command
                        answer = robot_local.make_action_question()   
                        #print(answer)

                        # TODO : replace by pre-answered questions
                        id_action += 1
                        id_action %= 2
                            
                    except :
                        print("error during intent")

                if 'arrêter' in command:
                    print("stop...")
                    break
                
            #thread_cond.release()

    except:
        print("Microphone doesn't work!")    

       
print("Starting Robot")
robot_local = Robot_Client()
#robot_local = Robot_Client(90,0)

key_word_listener = sr.Recognizer()
phrases_listener = sr.Recognizer()
with sr.Microphone() as source:
    micro_task(source)
