from cv.model import run_odt_and_draw_results
from robots.robot import Robot
import enums.state_robot as state_robot
import tensorflow as tf

from utils import faces_recognitions, write_name_over_bounding_box

N_FRAME = 10
THRESHOLD_DETECTION = 0.6

class Robot_Server(Robot) :

    # model interpreter
    interpreter = tf.lite.Interpreter(model_path="assets/model.tflite")
    interpreter.allocate_tensors()

    def make_action(self):
        if self.current_state == state_robot.RobotState.DETECTION:
            return self.make_action_detection()[0]
            
        if self.current_state == state_robot.RobotState.RECOGNITION:
            return self.make_action_recognition()
        
        if self.current_state == state_robot.RobotState.TRACKING:
            return self.make_action_tracking()
        
        if self.current_state == state_robot.RobotState.ANSWER_QUESTION:
            return self.make_action_question()
    
    def make_action_detection(self):
        # Call model 
        detection_result_image, boundings_boxs = run_odt_and_draw_results(
            self.frames[-1],
            None,
            self.interpreter,
            threshold=THRESHOLD_DETECTION,
            data_face_emb = []
        )

        return detection_result_image, boundings_boxs

    def make_action_recognition(self):
        delta = 10
        detection_result_image, boundings_boxs = self.make_action_detection()

        for bounding_box in boundings_boxs : 
            bbox = bounding_box["boundingBox"]
            face  = self.frames[-1][bbox[0]-delta:bbox[2]+delta,bbox[1]-delta:bbox[3]+delta]

            if bounding_box["classe"] == 0: 
                name_detect = faces_recognitions(self.faces_emb, face, bbox)
                detection_result_image = write_name_over_bounding_box(detection_result_image, bbox, name_detect)

        return detection_result_image

    def make_action_tracking(self):
        return
    

    def add_frame(self, frame):
        self.frames.append(frame)

        if(len(self.frames) > N_FRAME):
            self.frames.pop(0)