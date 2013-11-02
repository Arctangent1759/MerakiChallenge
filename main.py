import TourneyMaster
import os

MATCH_SYSTEM = "round robin"
ROUND_SYSTEM = "random"
PLAYER_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Players')

print "The tournament will be: ", MATCH_SYSTEM
tourney = TourneyMaster.TourneyMaster(_tournamentType=MATCH_SYSTEM, _roundSystem=ROUND_SYSTEM)
tourney.load_player_modules(PLAYER_DIRECTORY)
print "Ladies and gentleman, today's contestants are: ", tourney.get_player_names()
tourney.create_matches()
print "The matches are in! The matches are as follows: ", tourney.get_matches()
tourney.start_tourney()
winner = tourney.get_winner()
d = tourney.get_score()
for v in sorted(d, key=d.get, reverse=False):
  print v, d[v]
print "...and the winner is: ", winner
