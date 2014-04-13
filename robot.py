# robot.py -- sample liar's dice robot

import random,logging

RULES_FACES = 6 

def get_play(me,hands,history) :
    ''' raise to some random, possible, hand. call if impossible '''
    if 0 == len(history) :
        prev = 0,0
    else :
        x = int(history.split(',')[-1].split(':')[1])
        prev = x / 10,x % 10
    num_dice = sum(map(lambda x : len(x.split(':')[1]),hands.split(',')))

    # impossible?
    #
    if prev[0] > num_dice :
        return 0

    # top call?
    #
    if prev[0] == num_dice and prev[1] == 6 :
        return 0

    # loop till we find a bigger play
    #
    while 1 :
        qty = random.randint(prev[0],num_dice)
        face = random.randint(1,RULES_FACES)
        if (qty > prev[0]) or (qty == prev[0] and face > prev[1]) :
            return (qty * 10) + face

