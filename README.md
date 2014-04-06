liar's dice
===========

This is a game to pit [Liar's Dice][1] robots against each other.

You can write a robot by implementing the function:

    def get_move(me,hands,history) 

        me is the id of your player. eg, "A"

        hands is a serialization of each players hands, all 
        but your own will be masked until the hand is over
        e.g.:
            
            A:23135,B:..,C:....

        history is the history of plays. e.g.:

            A:23,B:33,C:0

        This means, player "A" called "two threes",
        player "B" called "three threes", player C 
        called "liar".

        Your function should return an integer 
        encoding the call, like, 23 for two threes,
        105 for 10 fives, or 0 for "liar".

For a quick start:

    % git clone git://github.com/colinmsaunders/liarsdice.git
    % cd liarsdice
    % python liarsdice.py games 1 players.p_human players.p_dummy

See [robot.py][2] for dox on how to write a robot.

- colinmsaunders@gmail.com

[1]: http://en.wikipedia.org/wiki/Liar's_dice
[2]: https://github.com/colinmsaunders/liarsdice/blob/master/robot.py
