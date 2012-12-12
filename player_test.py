# player_test.py -- template for creating a player to play letterpress

# Letterpress, by the way, is a sweet game for the iPhone, check it out:
#
#   https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8

# To write a player to play letterpress, create a file called my_player.py, 
# and implement the single function, ``get_move''.
# 
# You can then match your player against another using the letterpress.py
# script, like this:
#
#   % python letterpress.py game my_player their_player

# Your get_move() function should take three arguments: tiles, moves, and 
# colors, and return either None (indicating "pass"), or a vector of
# integer indexes into tiles, representing your word. For example, 
# if the top row of the board is c-z-o-w-a, and you want to play "cow",
# return (0,2,3) . 

# ``tiles'' is an array of 25 characters, representing the board. The 
# first character in the array is the top-left character, the sixth is 
# the first character in the second row.

# ``moves'' is a vector of moves so far. If moves is empty, this is the 
# first play, and you are the first player. If moves has one element, it is
# a new game, and you move second. A move is a tuple of zero-based indexes into
# tiles. 

# ``colors'' could be derived from tiles and moves, but we pass it in
# to make things easier for you. ``colors'' is an array of 25 integers, 
# representing the color of each tile. 
#
#   0   white (unowned)
#   1   dark blue (owned by player 1)
#   2   dark red (owner by player 2)

# get_move() is deliberately not object oriented, but you you're welcome to 
# fake it, if you want to create something in your constructor or at a new 
# game. Just check tiles to see if it is different than before, or keep a 
# hash of them in global scope. 

# Lastly, look at the other player_XXXX.py scripts for examples.


####################################################
#
# basic get_move() stub
#
####################################################

def get_move(tiles,moves,colors) :
    
    # TODO: write your algorithm here ...

    raise NotImplementedError


####################################################
#
# Or, with a class 
#
####################################################

class MyPlayer :
    def __init__(self,tiles) :
        self.tiles = tiles
    def get_move(self,moves,colors) :
        
        # TODO: write your algorithm here ...
        
        raise NotImplementedError


# the plumbing to instantiate the above ...

g_game = (None,None)

def get_move_RENAME_ME(tiles,moves,colors) :
    global g_game
    if tiles != g_game[0] :
        g_game = (tiles,MyPlayer(tiles))
    move = g_game[1].get_move(moves,colors)
    return move

