Liar's Dice
===========

This is a game to pit [Liar's Dice][1] robots against each other.

Liar's Dice is played amongst two or more players, each of which 
begin with a dice cup and 4 six-sided dice. All players roll their
dice, but don't reveal them. In turn, each player makes a declaration,
such as "two threes" or "three sixes", or, a player may call "Liar".
Each successive call must be higher than the previous (either a higher
quantity, or a higher face with the same quantity). These declarations
are for the *entire* set of dice combined. When a player calls "Liar",
all dice are revealed. If the assertion is met (that is, the number 
of faces is greater than or equal to the claim), then the player 
who called liar must remove a die from their cup. If not, the last
player to make the declaration must remove a die from their cup. If
a player has no more dice in their cup they are out of the game. 
Play continues in this fashion until only one player, the winner,
remains.

In this variation there are no wild dice, and no re-casting of dice.

You can write a robot by implementing the function:

    def get_play(me,hands,history) 

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

For a quick start to play against the computer:

    % git clone git://github.com/colinmsaunders/liarsdice.git
    % cd liarsdice
    % python main.py play human computer

See [robot.py][2] for dox on how to write a robot.

- colinmsaunders@gmail.com

[1]: http://en.wikipedia.org/wiki/Liar's_dice
[2]: https://github.com/colinmsaunders/liarsdice/blob/master/robot.py
