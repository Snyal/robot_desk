from enum import Enum

# Enumeration how describe vocal action state
# MECHANICAL : Ask robot to do a mecanical action (move/rotate/etcs)
# REQUEST : Ask robot to make a pre-know question
# OPEN_REQUEST : Ask robot to answer a open question (open IA)
class VocalActionType(Enum):
    MECHANICAL = 1
    REQUEST = 2
    OPEN_REQUEST = 3
