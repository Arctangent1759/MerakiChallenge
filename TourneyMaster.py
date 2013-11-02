import os
import itertools
import random
import traceback
import sys

import MatchMaster
from CheatingException import CheatingException

#bounds for number of rounds when generating randomly
RANDOM_LOWER_BOUND = 100
RANDOM_UPPER_BOUND = 150


def safe_dict_increment(d, k, a):
    if k not in d:
        d[k] = 0
    d[k] += a


class TourneyMaster:
    """
      The TourneyMaster's job is to load the player modules and execute
      a tournament. It is not interested in the details of what a match
      is; it leaves that to its MatchMaster to handle.
    """
    def __init__(self, _tournamentType="Round Robin", _roundSystem="random"):
        self.tournamentType = _tournamentType
        self.matches = []
        self.modules = []
        self.winCount = dict()
        self.numPlayers = None
        self.roundSystem = _roundSystem
        if self.roundSystem == "random":
            self.numRounds = random.randint(RANDOM_LOWER_BOUND,
                                            RANDOM_UPPER_BOUND)

    def load_player_modules(self, _directory=None):
        """
          Loads the names of the modules in a target directory.
        """
        assert _directory is not None
        self.directory = _directory
        for module in os.listdir(self.directory):
            fileExtension = module[-3:]
            if module == '__init__.py' or fileExtension != '.py':
                continue
            modName = ''.join(module[:-3])
            self.modules.append(modName)
        del module
        self.numPlayers = len(self.modules)

    def get_player_names(self):
        return list(self.modules)

    def get_matches(self):
        return list(self.matches)

    def create_matches(self):
        """
          Functionality depends on the type of tournament specified
          at initialization. For the default, round robin, this
          method will create a list of Matches which are tuples of
          player module references. For this reason, this method
          should only be called after a call to load_player_modules.
        """
        if self.tournamentType == "round robin":
            # A matching has size 2
            combinations = itertools.combinations(self.modules, 2)
            for pair in combinations:
                self.matches.append(pair)
            self.matches = self.matches * 1

    def handle_match_crash(self, match):
        tb = sys.exc_info()[2]
        stack = traceback.extract_tb(tb)
        crasher = None
        for s in stack:
            if s[2] == "get_move":
                crasher = s
        if crasher:
            crasher = os.path.splitext(os.path.basename(crasher[0]))[0]
            print "Match between", match[0], " and ",
            print match[1], " crashed"
            if crasher:
                print crasher, " Crashed!"

            safe_dict_increment(self.winCount, crasher, 1000)
        else:
            print "Match crashed, but unable to determine crasher"

    def run_match(self, match):
        matchMaster = MatchMaster.MatchMaster(match, self.directory,
                                              _numPlayers=2,
                                              _numRounds=self.numRounds)
        try:
            matchMaster.start_match()
        except CheatingException as e:
            cheater = str(e)
            print "Match between", match[0], " and ", match[1], " crashed"
            print cheater, "cheated"

            safe_dict_increment(self.winCount, cheater, 10000)
        except Exception as e:
            self.handle_match_crash(match)

        return matchMaster

    def start_tourney(self):
        """
          Iterates over its list of Matches and initializes a MatchMaster for
          each one. The MatchMaster is given the player modules in a match as
          input and takes care of executing the match. The TourneyMaster then
          takes the result and keeps a tally of the results to determine the
          winner.
        """
        matchCount = 1
        for match in self.matches:
            print "Match between ", match, " begins!"
            matchMaster = self.run_match(match)
            score = matchMaster.get_result()
            outcome = zip(match, score)
            index = 0
            # player_outcome = ('player name', matchScore)
            for player_outcome in outcome:
                if player_outcome[0] in self.winCount:
                    self.winCount[player_outcome[0]] += player_outcome[1]
                else:
                    self.winCount[player_outcome[0]] = player_outcome[1]
                index += 1
            print "Match between ", match, " has ended!"
            print "The score is: ", outcome
            print '\n', "*" * 70, '\n'
            matchCount += 1

    def get_score(self):
        return self.winCount

    def get_winner(self):
        """
          Returns the player with the lowest score.
        """
        return min(self.winCount, key=lambda k: self.winCount[k])
