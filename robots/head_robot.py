import RPi.GPIO as GPIO
import time

from utils import angle_to_percentage

class Head_Robot :

    current_x_angle = 90
    current_y_angle = 0

    def __init__(self, current_x_angle=90, current_y_angle = 0):
        self.current_x_angle = current_x_angle
        self.current_y_angle = current_y_angle

        self.init_head()

    def init_head(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # Set pun 11 & 12 as outputs, and define as PWM servo1 & 2
        GPIO.setup(11, GPIO.OUT)
        self.servo_up_down =  GPIO.PWM(11, 50) # pin 11 for servo1

        GPIO.setup(12, GPIO.OUT)
        self.servo_left_right =  GPIO.PWM(12, 50) # pin 12 for servo1

        self.servo_left_right.start(angle_to_percentage(self.current_x_angle))
        self.servo_up_down.start(angle_to_percentage(self.current_y_angle))
        
    # TODO : make robuste to < 0
    def rotate_head(self, angle_x=0, angle_y=0):        

        p_angle_x = angle_to_percentage(angle_x)
        p_angle_y = angle_to_percentage(angle_y)
        
        if angle_x !=  self.current_x_angle :
            self.servo_left_right.ChangeDutyCycle(p_angle_x)

        if angle_y !=  self.current_y_angle :   
            self.servo_up_down.ChangeDutyCycle(p_angle_y)
        
        time.sleep(0.5)
        
        self.servo_left_right.ChangeDutyCycle(0)
        self.servo_up_down.ChangeDutyCycle(0)
        
        # update new angles
        self.current_x_angle = angle_x
        self.current_y_angle = angle_y

        print("x angle = ", self.current_x_angle)
        print("y angle = ", self.current_y_angle)