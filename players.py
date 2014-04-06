# players.py -- some sample players

import random

def p_caller(me,hands,history) :
    'always call'
    return 0

def p_human(me,hands,history) : 
    print 'You are "%s".   Hands: %s    History: %s' % (me,hands,history)
    print 'Enter move (0 to call, or 23 for two threes, 106 for ten sixes):'
    s = raw_input()
    return int(s)

def p_bumper(me,hands,history) :
    ''' just bump previous call '''
    if 0 == len(history) :
        return 11   # "one one"
    prev = history.split(',')
    last_play = prev[-1]
    last_player,last_call = last_play.split(':')
    last_call = int(last_call)
    # ignore showdown
    if 0 == last_call :
        return 0
    last_face = last_call % 10
    last_quantity = last_call / 10
    if 6 == last_face :
        return ((last_quantity + 1) * 10) + 1
    return (last_quantity * 10) + (last_face + 1)

def p_simpleton(me,hands,history) :
    ''' play lowest call i can amongst faces i have '''
    hands = hands.split(',')
    my_hand = [0,0,0,0,0,0]
    for i in hands :
        player,dice = i.split(':')
        if me == player :
            for j in dice :
                my_hand[int(j) - 1] += 1
            break

    if 0 == len(history) :
        last_call = 0
        last_face = 0
        last_quantity = 0
    else :
        prev = history.split(',')
        last_play = prev[-1]
        last_player,last_call = last_play.split(':')
        last_call = int(last_call)
        if 0 == last_call :
            return 0
        last_face = last_call % 10
        last_quantity = last_call / 10

    if 0 == len(history) :
        quantity = 1
    else :
        quantity = last_quantity
    while 1 :
        for face in (1,2,3,4,5,6) :
            if 0 == my_hand[face - 1] :
                continue
            if quantity > last_quantity or face > last_face :
                return (quantity * 10) + face
        quantity += 1

