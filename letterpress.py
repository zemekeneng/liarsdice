#!/usr/bin/python

# letterpress.py -- play letterpress
#
#   https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8
#

HELP = '''\
letterpress.py -- this program pits letterpress algorithms against each other

Play a game between algo_123.py and algo_common_threes.py:

    % python letterpress.py game algo_123 algo_common_threes

Plays 100 round robin games between algo_123.py, algo_common_threes.py, and 
algo_my_algo, using seed "seed".

    % python letterpress.py tournament 100 seed algo_123 algo_common_threes algo_my_algo

See algo_test.py for documentation on how to write a player.
'''

MAX_TIME_PER_GAME = 60

import sys,logging,os,random,time

g_sowpods = None
def word_in_sowpods(word) :
    global g_sowpods
    if None == g_sowpods :
        g_sowpods = {}
    for i in file('sowpods.txt').readlines() :
        g_sowpods[i[:-1]] = 1
    return word in g_sowpods

def play_game(rng,player_1,player_2) :

    # set up the game
    #
    moves = []
    colors = []
    for i in range(25) :
        colors.append(0)
    clocks = [0.0,0.0]
    whose_move = 1
    tiles = ''
    for i in range(25) :
        tiles += random.choice('abcdefghijklmnopqrstuvwxyz')
    logging.info('tiles: %s' % tiles)

    # put the players in a tuple so we can flip back and forth 
    #
    players = (player_1,player_2)
    
    # keep playing until someone makes an illegal move,
    # or the last two moves were passes
    #
    disqualified = None
    while 1 :
        
        # get the player's move
        #
        started = time.time()
        try :
            move = players[whose_move - 1](tiles[:],moves[:],colors[:])
            logging.info('player %d returned %s' % (whose_move,str(move)))
        except :
            logging.info('player %d threw an exception ("%s"), disqualifying ...' % (whose_move,str(sys.exc_info()[:2])))
            disqualified = whose_move
            break

        # did they take too long?
        #
        elapsed = time.time() - started
        clocks[whose_move - 1] += elapsed
        if MAX_TIME_PER_GAME < clocks[whose_move - 1] :
            logging.info('player %d took too long, disqualifying ...' % (whose_move,))
            disqualified = whose_move
            break

        # did they pass? if so, check if game is over, otherwise continue
        #
        if None == move :
            moves.append(move)
            if 2 <= len(moves) and None == moves[-2] :
                logging.info('last two plays were passes, breaking ...')
                break
            whose_move = {1:2,2:1}[whose_move]
            continue
                
        # ok, they played a word, make sure it is a legal play
        #
        word = ''
        try :
            move = tuple(move)
            used = {}
            for i in move :
                if i in used :
                    logging.info('player %d used %s twice, disqualifying ...' % (whose_move,str(i)))
                    disqualified = whose_move
                    break
                used[i] = 1
                word += tiles[i]
        except :
            logging.info('player %d returned an illegal move: %s, disqualifying ...' % (whose_move,str(play)))
            disqualified = whose_move
            break

        if None != disqualified :
            break

        # in dictionary?
        #
        if not word_in_sowpods(word) :
            logging.info('player %d played word not in dictionary (%s), disqualifying ...' % (whose_move,word))
            disqualified = whose_move
            break

        # already been played?
        #
        for i in moves :
            if word == ''.join(map(lambda x : tiles[x],i[:len(word)])) :
                logging.info('player %d played word (%s) already played (%s), disqualifying ...' % (whose_move,word,i))
                disqualified = whose_move
                break
        if None != disqualified :
            break

        # looks good, let's play it
        #
        logging.info('player %d played %s ("%s") ...' % (whose_move,str(move),word))
        moves.append(move)

        # update the colors
        #
        new_colors = []
        for i in move :
            
            # make sure it isn't surrounded
            #
            surrounded = True
            x = i % 5 
            y = i / 5
            if surrounded and x > 0 and colors[i - 1] in (0,whose_move) :
                surrounded = False
            if surrounded and x < 4 and colors[i + 1] in (0,whose_move) :
                surrounded = False
            if surrounded and y > 0 and colors[i - 5] in (0,whose_move) :
                surrounded = False
            if surrounded and y < 4 and colors[i + 5] in (0,whose_move) :
                surrounded = False

            if not surrounded :
                new_colors.append(i)

        for i in new_colors :
            colors[i] = whose_move 

        # flip whose_move and continue
        #
        whose_move = {1:2,2:1}[whose_move]
        continue

    # did someone get disqualified?
    #
    if None != disqualified :
        return {1:2,2:1}[disqualified]

    # nope, let's count colors
    #
    points = [0,0,0]
    for i in colors :
        points[i] += 1

    logging.info('game over, white: %d, player 1: %d, player 2: %d' % (points[0],points[1],points[2]))
       
    # all done, return result
    #
    if 0 :
        pass
    elif points[1] > points[2] :
        logging.info('player 1 wins')
        return 1   
    elif points[2] > points[1] :
        logging.info('player 2 wins')
        return 2
    else :
        logging.info('tie game')
        return 0

def make_player(s) :
    try :
        m = __import__(s)
    except :
        logging.warn('couldn\'t import "%s"' % s)
        return None
    f = getattr(m,'get_move')
    return f

def tournament(n,seed,player_names) :
    rng = random.Random(seed)
    players = {}
    for i in player_names :
        player_id = 'p%d__%s' % (len(players) + 1,i)
        logging.info('making player %s ...' % player_id)
        p = make_player(i)
        players[player_id] = p
    results = {}
    for r in range(n) :
        for p1 in players.keys() :
            for p2 in players.keys() :
                if p1 == p2 :
                    continue
                logging.info('playing game between %s and %s ...' % (p1,p2))
                result = play_game(rng,players[p1],players[p2])
                if not results.has_key((p1,p2)) :
                    results[(p1,p2)] = []
                results[(p1,p2)].append(result)
    return results

def single_game(seed,player_name_1,player_name_2) :
    rng = random.Random(seed)
    logging.info('making player %s ...' % player_name_1)
    p1 = make_player(player_name_1)
    logging.info('making player %s ...' % player_name_2)
    p2 = make_player(player_name_1)
    logging.info('playing game between %s and %s ...' % (player_name_1,player_name_2))
    result = play_game(rng,p1,p2)
    if 0 == result :
        logging.info('tie game')
    if 1 == result :
        logging.info('%s won' % player_name_1)
    if 2 == result :
        logging.info('%s won' % player_name_2)

def main(argv) :
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',stream=sys.stdout)
    if 1 == len(argv) :
        print HELP
        sys.exit()

    c = argv[1]

    if 0 :
        pass

    elif 'help' == c :
        print HELP
        sys.exit()

    elif 'game' == c :
        seed = None
        if 5 == len(sys.argv) :
            seed = sys.argv[4]
        single_game(seed,sys.argv[2],sys.argv[3])

    elif 'tournament' == c :
        tournament(int(sys.argv[2]),sys.argv[3],sys.argv[4:])

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

