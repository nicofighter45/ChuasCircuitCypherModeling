from enum import Enum

class State(Enum):
    PREPARATION = 0
    NOMINAL = 1
    GRAPHS = 2



print(State.GRAPHS == True)
