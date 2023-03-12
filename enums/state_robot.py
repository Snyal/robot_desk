from enum import Enum

# Enumeration how describe robot state
# Detection : Detect objet know by robot 
# Recognition : Detect person(s)
# Tracking : Track a person/object
class RobotState(Enum):
    DETECTION = 1
    RECOGNITION = 2
    TRACKING = 3
    ANSWER_QUESTION = 4

ROBOT_STATE = Enum('RobotState', ['DETECTION', 'RECOGNITION', 'TRACKING'])