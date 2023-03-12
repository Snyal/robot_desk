from enum import Enum
import numpy as np

# Object Detection
import enums.state_robot as state_robot

class Robot :
    # set default state from robot
    current_state = state_robot.RobotState.DETECTION

    # last N_frames seen by robot camera
    frames = []

    # TODO : move -> add load
    #faces_emb = faces_encodings()
    faces_emb = np.load("assets/faces_encodings.npy", allow_pickle = True)

    def make_action(self):
        return
    
    def change_state(self, new_state_id):

        if new_state_id == 0 : 
            self.current_state = state_robot.RobotState.DETECTION
        
        if new_state_id == 1 : 
            self.current_state = state_robot.RobotState.RECOGNITION

        if new_state_id == 2 : 
            self.current_state = state_robot.RobotState.TRACKING

        if new_state_id == 3 : 
            self.current_state = state_robot.RobotState.ANSWER_QUESTION

    def debug(self):
        print("nb_frames : ", len(self.frames))
            

