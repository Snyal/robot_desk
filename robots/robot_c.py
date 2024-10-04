import json
import numpy as np
import openai
from robots.head_robot import Head_Robot
from robots.robot import Robot
import enums.state_robot as state_robot

OPENAI_KEY = ""

class Robot_Client(Robot) :
    head_Robot = None
    
    openai.api_key = OPENAI_KEY
    completion = openai.Completion()

    question = ""
    humans = {}
    current_bounding_box = np.array([])

    def __init__(self):
        self.head_Robot = None
        self.init_humans_data()
        
    def __init__(self, head_x_angle=90, head_y_angle = 0):
        self.init_humans_data()
        self.head_Robot = Head_Robot(head_x_angle,head_y_angle)
    
    def make_action(self):
        if self.current_state == state_robot.RobotState.ANSWER_QUESTION:
            return self.make_action_question()
    
    def make_action_question(self, chat_log=None):

        id_action = 1

        if "photo" in self.question :
            answer = "Prise de photo"
            id_action = 5
        else :
            prompt = f'{chat_log}Human: {self.question}\nAI:'
            response = self.completion.create(
                prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
                top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
                max_tokens=150)
            answer = response.choices[0].text.strip()
    
        return answer, id_action
            
    # ------ JSON ------
    def init_humans_data(self):
        f = open("assets/humans_data.json")
        self.humans = json.load(f)
        f.close()

    def get_humans_information(self, id) :
        for human in self.humans:
            if human["id"] == id  :
                return human
          
        
