# robot.py -- template for creating a player to play liar's dice

# How to Write a Robot
# ====================
#
# Your robot's get_play() function will be called for each 
# play, and once at the end of each hand (even if already 
# out of the game).
#
# The get_play() prototype looks like:
#
#   def get_play(me,hands,history)
#
#       me is the id of your player. eg, "A"
#
#       hands is a serialization of each players hands, all 
#       but your own will be masked until the hand is over
#       e.g.:
#            
#           A:23135,B:..,C:....
#
#        history is the history of plays. e.g.:
#
#            A:23,B:33,C:0
#
#        This means, player "A" called "two threes",
#        player "B" called "three threes", player C 
#        called "liar".
#
#        Your function should return an integer 
#        encoding the call, like, 23 for two threes,
#        105 for 10 fives, or 0 for "liar".
#
# see players.py for some sample players, or, copy this file and implement the 
# following function

def get_move(me,hands,history,rules) :
    return 0

