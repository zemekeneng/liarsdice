test harness for pitting letterpress strategies against one another

quick start:


    % python letterpress.py games 100 abc foo foo

This plays foo against foo 100 times with seed "abc". 

foo.py looks like:

    def get_play(tiles,colors,moves) :
	    return (0,1,2)

* tiles is an array of 25 characters
* colors is an array of 25 ints 
    0 means empty
    1 means owned by player 1 
    2 means owned by player 2 
* moves is an ordered list of moves

get_play() should return an ordered list of indexes into tiles; 0 is the top left,
4 is the left-most tile on the second row.

