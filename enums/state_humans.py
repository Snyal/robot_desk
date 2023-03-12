from enum import Enum

class Situation(Enum):
    SINGLE = 0
    COUPLE = 1
    PARENT = 2
    SISTER_BROTHER = 3
    GRAND_PARENT = 4
    KIDS = 5

SITUATION = Enum('SITUATION', ['SINGLE', 'COUPLE', 'PARENT', 'SISTER_BROTHER', 'GRAND_PARENT'])

class Gender(Enum):
    MISTER = 0
    WOMEN = 1
    ANIMAL = 2

GENDER = Enum('GENDER', ['MISTER', 'WOMEN', 'ANIMAL'])
