# players.py -- some sample players

import random,logging

def p_caller(me,hands,history,rules) :
    'always call'
    return 0

def p_human(me,hands_str,history,rules) : 
    logging.info('You are player "%s".' % me)
    logging.info('History: %s' % history)
    logging.info('Hands: %s' % hands_str)
    if 0 != len(history) :
        last_play = history.split(',')[-1]
        if 0 == int(last_play.split(':')[1]) :
            logging.info('Hand over. Press return to continue ...')
            raw_input()
            logging.info('*' * 50)
            return
    logging.info('Enter move (e.g., "0" to call, "23" for two threes, "106" for ten sixes) :')
    s = raw_input()
    x = 0
    try :
        x = int(s)
    except :
        pass
    logging.info('*' * 50)
    return x

def p_bumper(me,hands,history,rules) :
    ''' just bump previous call '''
    if 0 == len(history) :
        return 11   # "one one"
    last_play = history.split(',')[-1]
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

def p_simpleton(me,hands,history,rules) :
    ''' play lowest call i can amongst faces i have '''
    hands = hands.split(',')
    my_hand = {}
    my_max_face = 0
    for i in hands :
        player,dice = i.split(':')
        if me == player :
            for j in dice :
                j = int(j)
                if j > my_max_face :
                    my_max_face = j
                my_hand[j] = my_hand.get(j,0) + 1
            break
    if 0 == len(history) :
        last_call = 0
        last_face = 0
        last_quantity = 0
    else :
        last_play = history.split(',')[-1]
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
        for face in range(1,my_max_face + 1) :
            if 0 == my_hand.get(face,0) :
                continue
            if quantity > last_quantity or face > last_face :
                return (quantity * 10) + face
        quantity += 1

def p_conservative(me,hands,history,rules) :
    ''' only play things i have, otherwise call '''
    hands = hands.split(',')
    my_hand = {}
    my_max_face = 0
    my_dice = 0
    for i in hands :
        player,dice = i.split(':')
        if me == player :
            for j in dice :
                my_dice += 1
                j = int(j)
                if j > my_max_face :
                    my_max_face = j
                my_hand[j] = my_hand.get(j,0) + 1
            break

    if 0 == len(history) :
        last_call = 0
        last_face = 0
        last_quantity = 0
    else :
        last_play = history.split(',')[-1]
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
        for face in range(1,my_max_face + 1) :
            if quantity > my_hand.get(face,0) :
                continue
            if quantity > last_quantity or face > last_face :
                return (quantity * 10) + face
        quantity += 1
        if quantity > my_dice :
            return 0

