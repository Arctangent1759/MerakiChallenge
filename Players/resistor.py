import Game

class Player():
    def __init__(self, _scoreboard, _ID):
        self.scoreboard = _scoreboard
        self.ID = _ID

    def get_move(self):
        return Game.STAY_SILENT
