#!/usr/bin/python

# play letterpress
#
#   https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8
#

import sys,logging,os,random,time

def show_help() :
    print '''\
letterpress.py -- this program pits letterpress algorithms against each other

Play a game between algo_123.py and algo_common_threes.py:

    % python letterpress.py game algo_123 algo_common_threes

Plays 100 round robin games between algo_123.py, algo_common_threes.py, and 
algo_my_algo, using seed "seed".

    % python letterpress.py tournament 100 seed algo_123 algo_common_threes algo_my_algo

See algo_test.py for documentation on how to write a player.
'''

def play_game(rng,player_1,player_2) :
    # TODO: implement
    return rng.choice((0,1,2))

def make_player(s) :
    try :
        m = __import__(s)
    except :
        logging.warn('couldn\'t import "%s"' % s)
        return None
    f = getattr(m,'get_play')
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
        show_help()
        sys.exit()

    c = argv[1]

    if 0 :
        pass

    elif 'help' == c :
        show_help()
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
        show_help()
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

