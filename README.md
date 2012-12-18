letterpress
===========

This is a test harness for pitting letterpress robots against one
another. 

[Letterpress][1] is a game for the iPhone, a two player cross between
scrabble and go.

You can write a robot by implementing the function:

    def get_move(tiles,moves,colors) 

For a quick start:

    % git clone git://github.com/colinmsaunders/letterpress.git
    % cd letterpress
    % python letterpress.py game players.p_human players.p_random 

See [robot.py][2] for dox on how to write a robot.


- colinmsaunders@gmail.com

[1]: https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8
[2]: https://github.com/colinmsaunders/letterpress/blob/master/robot.py
