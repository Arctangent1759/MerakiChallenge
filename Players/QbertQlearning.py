import Game
from random import choice
from random import random

# CONSTANTS
EPSILON_DAMPING=1.5 #How quickly experimentation decreases over time.
ALPHA = 0.1


class Player():
    def __init__(self, _scoreboard, _ID):
        self.scoreboard = _scoreboard
        self.ID = _ID
        self.qValues={
                      'start': {Game.RAT_OUT: 0, Game.STAY_SILENT: 0},
                      'rat_out': {'wait': 0},
                      'stay_silent': {'wait': 0},
                      'opp_rat_out': {'exit': 0},
                      'opp_stay_silent': {'exit': 0}
                      }
        self.lastAction=None
        
    def get_move(self):
        roundNum=self.scoreboard.get_round_number()
        if roundNum==0:
            action = choice([Game.RAT_OUT,Game.STAY_SILENT])
            self.lastAction=action
            return action
        else:
            #Update Q-Values
            my_last_action='rat_out' if self.scoreboard.get_player_move(roundNum-1,self.ID)==Game.RAT_OUT else 'stay_silent'
            opp_last_action='opp_rat_out' if self.scoreboard.get_other_player_move(roundNum-1,self.ID)==Game.RAT_OUT else 'opp_stay_silent'
            last_episode = [('start',self.lastAction,my_last_action),(my_last_action,'wait',opp_last_action)]
            
            for startState, action, endState in last_episode:
                self.update(startState, action, endState)    
                
            if random() <= self.learningFunction():
                action = choice([Game.RAT_OUT,Game.STAY_SILENT])
            else:
                action = self.computeActionFromQValues('start')
        return action

    def learningFunction(self):
        return 1.0/(1.0+EPSILON_DAMPING*self.scoreboard.get_round_number())
    
    def getQValue(self, state, action):
        return self.qValues[state][action]
    
    def computeValueFromQValues(self, state):
        return max([self.qValues[state][action] for action in self.qValues[state].keys()])
    
    def computeActionFromQValues(self, state):
        actions = self.qValues[state].keys()
        bestAction = ''
        bestValue = float('-inf')
        for action in actions:
            currValue = self.qValues[state][action]
            if currValue > bestValue:
                bestAction = action
                bestValue = currValue
        return bestAction
    
    def update(self, state, action, nextState):
        self.qValues[state][action] = ((1-ALPHA) * self.getQValue(state, action)) + ((ALPHA) * (getReward(state, action, nextState) + self.computeValueFromQValues(state)))

def getReward(startState, action, endState):
    if startState=='start' or action=='exit':
        return 0
    else:
        myAction = (Game.RAT_OUT if startState=='rat_out' else Game.STAY_SILENT)
        oppAction = (Game.RAT_OUT if startState=='opp_rat_out' else Game.STAY_SILENT)
        return -Game.solve(myAction,oppAction)[0]
