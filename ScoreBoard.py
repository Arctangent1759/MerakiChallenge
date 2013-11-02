import inspect
import os
from CheatingException import CheatingException


class ScoreBoard:
    """
      ScoreBoard is an object meant to be shared by MatchMaster and the players.
      It is published to by MatchMaster and subscribed to by the players.
    """
    def __init__(self, _numPlayers, secret):
        self.results = []
        self.moves = []
        self.roundNum = 0
        self.numPlayers = _numPlayers
        self.score = [0] * self.numPlayers
        self.__secret = secret
        self.__valid = True

    def enter_round_data(self, secret, moves, result):
        """
          MatchMaster's way of updating the ScoreBoard with the moves and results
          of a new round.
        """
        if secret != self.__secret:
            self.__valid = False
            stack = inspect.stack()
            thes = None
            for s in stack:
                if s[3] == "get_move":
                    thes = s
            self.__player_name = os.path.splitext(os.path.basename(thes[1]))[0]

        if not self.__valid:
            raise CheatingException(self.__player_name)

        assert len(moves) == self.numPlayers
        assert len(result) == self.numPlayers
        self.moves.append(moves)
        self.results.append(result)
        self.roundNum += 1

    def get_result(self, roundNum):
        """
          Returns a tuple of form (punishment for p1, punishment for p2)
          for the round denoted by roundNum.
        """
        return self.results[roundNum]

    def get_score(self):
        """
          Returns a tuple of form (p1 score, p2 score).
        """
        return tuple(self.score)

    def get_round_number(self):
        return self.roundNum

    def get_player_move(self, roundNum, player):
        """
          Returns the Move.* done by player in round roundNum.
        """
        return (self.moves[roundNum])[player]

    def get_other_player_move(self, roundNum, yourID):
        """
          Returns the Move.* done by the other player in round roundNum.
        """
        return self.get_player_move(roundNum, yourID ^ 1)
