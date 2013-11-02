import random
import sys
import time

import ScoreBoard
import Game

class MatchMaster:
    """
    The MatchMaster exceutes a match between two player modules.
    The game is irrelevant to the MatchMaster.
    Its duties include:
        1. Loading the modules and instantiating the player objects
        2. Managing the ScoreBoard, a shared object between players
        3. Asking the players for moves
        4. Preparing results for the TourneyMaster
    """
    def __init__(self, moduleNames, directory, _numPlayers=2, _numRounds=None):
        """
        Instantiates player objects and Scoreboard.
        """
        self.playerModules = []
        self.players = []
        playerID = 0

        self.numRounds = _numRounds
        self.secret = random.random()
        self.scoreBoard = ScoreBoard.ScoreBoard(_numPlayers, self.secret)
        sys.path.append(directory)
        for moduleName in moduleNames:
            currModule = __import__(moduleName)
            self.playerModules.append(currModule)
            self.players.append(currModule.Player(self.scoreBoard, playerID))
            playerID += 1

        self.scores = [0] * _numPlayers
        #dict([(player:0) for player in self.players])

    def start_match(self, matchType="IPD"):
        """
        Starts a match and returns when match is over.
        """
        if matchType == "IPD":  # IPD = Iterated Prisoner's Dilemma
            player1, player2 = self.players
            results = []
            for ipd_round in range(self.numRounds):
                move1 = player1.get_move()  # implement scoreboard deepcopying
                move2 = player2.get_move()
                if Game.communication_failed(): move1 = Game.opposite_move(move1)
                if Game.communication_failed(): move2 = Game.opposite_move(move2)
                player1Res, player2Res = Game.solve(move1, move2)
                results.append("(" + str(player1Res) + ", " + str(player2Res) + ")")
                self.scores[0] += player1Res
                self.scores[1] += player2Res
                self.scoreBoard.enter_round_data(self.secret, (move1, move2),
                                                 (player1Res, player2Res))
        print "Match results: [" + ", ".join(results) + "]"


    def get_result(self):
        """
        Returns a dictionary of scores from the match
        """
        return self.scores
