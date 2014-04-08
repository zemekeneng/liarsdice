# liarsdice.py -- the liar's dice logic functions, you can import this in your robots

# the variation of liars dice (4 6-sided dies, ones not wild)
#
RULES_DICE          = 4
RULES_FACES         = 6
RULES_ONES_WILD     = 0

STR_FACE_SINGLE = {
    1   : 'one',
    2   : 'two',
    3   : 'three',
    4   : 'four',
    5   : 'five',
    6   : 'six',
    7   : 'seven',
    8   : 'eight',
    9   : 'nine',
}

STR_FACE_PLURAL = {
    1   : 'ones',
    2   : 'twos',
    3   : 'threes',
    4   : 'fours',
    5   : 'fives',
    6   : 'sixes',
    7   : 'sevens',
    8   : 'eights',
    9   : 'nines',
}

STR_QUANTITY = {
    1   : 'one',
    2   : 'two',
    3   : 'three',
    4   : 'four',
    5   : 'five',
    6   : 'six',
    7   : 'seven',
    8   : 'eight',
    9   : 'nine',
}

import random,logging,sys

def verbose_play(play) :
    if 0 :
        pass
    elif 0 == play :
        return 'LIAR!'
    elif 1 == (play / 10) :
        return 'one %s' % STR_FACE_SINGLE.get(play % 10,'???')
    else :
        return '%s %s' % (STR_QUANTITY.get(play / 10,'%d' % (play / 10)),STR_FACE_PLURAL.get(play % 10,'???'))

def parse_history(history_str) :
    a = []
    h = history_str.split(';')
    for i in h :
        a.append(i.split(':'))
    return a

def parse_hands(hands_str) :
    a = []
    h = hands_str.split(';')
    for i in h :
        a.append(i.split(':'))
    return a

def my_hand(me,hands_str) :
    for i in parse_hands(hands_str) :
        if i[0] == me :
            return i[1]
    return None

def count_dice(hands_str) :
    t = 0
    for i in parse_hands(hands_str) :
        t += len(i[1])
    return t

def play_game(players,catch_exceptions) :
    
    # first, set up the players left in the game
    #
    seats = players.keys()
    random.shuffle(seats)
    whose_move = 0
    cups = {}
    dice = RULES_DICE
    faces = RULES_FACES
    for i in seats :
        cups[i] = dice

    logging.info('=' * 50)
    logging.info('new game between %s' % ', '.join(seats))

    # keep playing hands until only one player left
    #
    while 1 :

        # only one player left?
        #
        winner = None
        for i in seats :
            if 0 != cups[i] :
                if None != winner :
                    winner = None
                    break
                winner = i
        if None != winner :
            break

        # everyone rolls their dice
        #
        logging.info('-' * 50)
        logging.info('new hand between %s with %s dice, respectfully' % (', '.join(filter(lambda x : 0 != cups[x],seats)),', '.join(map(lambda x : '%d' % cups[x],filter(lambda x : 0 != cups[x],seats)))))
        hands = {}
        for i in seats :
            if 0 == cups[i] :
                continue
            hands[i] = []
            logging.debug('rolling %d dice for %s ...' % (cups[i],i))
            for j in range(cups[i]) :
                hands[i].append(random.randint(1,faces))
        logging.debug('hands: %s' % str(filter(lambda x : 0 != cups[x[0]],hands.items())))
        
        # keep playing hands until someone calls liar
        #
        history = []
        while 1 :
            
            logging.debug('getting move from %s ...' % seats[whose_move])

            # build history
            #
            history_str = ','.join(map(lambda x : '%s:%d' % (seats[x[0]],x[1]),history))

            # build hands
            #
            hands_str = None
            for i in seats :
                if None == hands_str :
                    hands_str = ''
                else :
                    hands_str += ','
                if i == seats[whose_move] :
                    hands_str += '%s:%s' % (seats[whose_move],''.join(map(lambda x : str(x),hands[seats[whose_move]])))
                else :
                    hands_str += '%s:%s' % (i,'x' * cups[i])

            # get the play
            #
            play = 0
            try :
                play = int(players[seats[whose_move]](seats[whose_move],hands_str,history_str))
            except KeyboardInterrupt :
                raise
            except :
                if not catch_exceptions :
                    raise
                logging.warn('caught exception "%s" calling %s\'s get_play() function' % (sys.exc_info()[1],seats[whose_move]))
            logging.info('player %s calls "%s"' % (seats[whose_move],verbose_play(play)))

            # check for legal moves
            # 
            if 0 != play :
                face = play % 10
                quantity = play / 10
                if face <= 0 or face > faces or quantity <= 0 or quantity > (len(players) * dice) :
                    logging.info('illegal move, assuming calling liar')
                    play = 0
                elif 0 != len(history) :
                    last_play = history[-1][1]
                    last_face = last_play % 10
                    last_quantity = last_play / 10
                    if (quantity < last_quantity) or ((quantity == last_quantity) and (face <= last_face)) :
                        logging.info('not increasing play, assuming calling liar')
                        play = 0

            # remember the play
            #
            history.append((whose_move,play))
            
            # if it's a call, or an illegal move, or a bet less than the last play
            # treat it as a call and check the bluff
            #
            loser = None
            if 0 == play :
                
                # if it's the first play, they lose
                #
                if 1 == len(history) :
                    logging.debug('called liar before any plays')
                    loser = seats[whose_move]

                else :
                    
                    # count dice
                    #
                    common_dice = {}
                    for i in seats :
                        if 0 == cups[i] :
                            continue
                        for j in hands[i] :
                            common_dice[j] = common_dice.get(j,0) + 1
 
                    last_play = history[-2][1]
                    last_face = last_play % 10
                    last_quantity = last_play / 10
 
                    logging.debug('hands: %s' % str(hands))
                    logging.debug('common dice: %s' % str(common_dice))

                    logging.info('player %s calls liar on player %s\'s call of %s' % (seats[whose_move],seats[history[-2][0]],verbose_play(last_play)))
                    logging.info('hands: %s' % ', '.join(map(lambda x : '%s:%s' % (x,''.join(map(lambda y : str(y),hands[x]))),filter(lambda x : 0 != cups[x],seats))))
                    logging.info('common dice: %s' % ', '.join(map(lambda x : verbose_play((x[1] * 10) + x[0]),common_dice.items())))

                    if common_dice.get(last_face,0) >= last_quantity :
                        logging.debug('%s\'s last play was %d %d\'s, CORRECT, %s loses' % (seats[history[-2][0]],last_quantity,last_face,seats[whose_move]))
                        loser = seats[whose_move]
                    else :
                        logging.debug('%s\'s last play was %d %d\'s, INCORRECT, %s loses' % (seats[history[-2][0]],last_quantity,last_face,seats[history[-2][0]]))
                        loser = seats[history[-2][0]]

                # remove loser's die, bump them if they're out of dice,
                # and start over again
                #
                # show everyone the result
                #
                logging.debug('showing everyone the result')
                history_str = ','.join(map(lambda x : '%s:%d' % (seats[x[0]],x[1]),history))
                hands_str = ','.join(map(lambda x : '%s:%s' % (x,''.join(map(lambda y : str(y),hands[x]))),filter(lambda x : 0 != cups[x],seats)))
                logging.info('player %s loses one die' % loser)
                cups[loser] -= 1
                if 0 == cups[loser] :
                    logging.info('player %s has no dice left' % loser)
                for i in seats :
                    try :
                        players[i](i,hands_str,history_str)
                    except KeyboardInterrupt :
                        raise
                    except :
                        if not catch_exceptions :
                            raise
                        logging.warn('caught exception "%s" calling %s\'s get_play() function' % (sys.exc_info()[1],i))
              
            # advance next move
            #
            while 1 :
                whose_move += 1
                if whose_move == len(seats) :
                    whose_move = 0
                if 0 != cups[seats[whose_move]] :
                    break

            # new hand if necessary
            #
            if None != loser :
                break

    logging.info('player %s wins' % winner)
    return winner

