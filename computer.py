# computer.py -- sample liar's dice robot

import random,logging

def get_play(me,hands,history) :
    
    # figure out the previous call
    #
    if 0 == len(history) :
        prev_quantity,prev_face = 0,0
    else :
        x = int(history.split(',')[-1].split(':')[1])
        prev_quantity,prev_face = x / 10,x % 10
    
    # count the total number of dice
    #
    num_dice = sum(map(lambda x : len(x.split(':')[1]),hands.split(',')))
 
    # find my hand
    #
    my_hand = None
    for i in hands.split(',') :
        who,dice = i.split(':')
        if who == me :
            my_hand = dice
            break

    # try 4 times to find pick
    # a random better play, if
    # can't, just call
    #
    for i in range(4) :

        # pick a random face from my dice
        #
        face = int(my_hand[random.randint(0,len(my_hand) - 1)])

        # pick a random quantity from 1 to the
        # total number of dice, but skew it low
        #
        quantity = 1 + int(abs(random.normalvariate(0.0,num_dice / 4.0)))

        logging.debug('trying %d %d\'s ...' % (quantity,face))

        # is it a bigger call than the previous?
        #
        if (quantity > prev_quantity) or ((quantity == prev_quantity) and (face > prev_face)) :

            # if so, return it
            #
            return (quantity * 10) + face

    # nothing found, just call
    # 
    logging.debug('nothing found, calling ...')
    return 0

