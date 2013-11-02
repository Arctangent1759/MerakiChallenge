# valid moves
import random
RAT_OUT = 0
STAY_SILENT = 1

# payoff matrix
results = {
    (RAT_OUT, RAT_OUT): (2, 2),
    (RAT_OUT, STAY_SILENT): (0, 3),
    (STAY_SILENT, RAT_OUT): (3, 0),
    (STAY_SILENT, STAY_SILENT): (1, 1)
}

def solve(move1, move2):
    return results[(move1, move2)]

def opposite_move(move):
    return (STAY_SILENT if move == RAT_OUT else  RAT_OUT)

def communication_failed():
    return random.randint(0, 9) == 0
