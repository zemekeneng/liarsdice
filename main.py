#!/usr/bin/python

# main.py -- console liar's dice test harness

HELP = '''\
usage:

    To play against the computer:

        $ python main.py human

    To play against your robot in my_robot.py named get_play():

        $ python main.py human my_robot.get_play

    To play 10 games of liar's dice between get_play() in my_robot.py, get_play in 
    his_robot.py, and dummy() in robots.py.
    
        $ python main.py play 10 my_robot.get_play his_robot.get_play robots.dummy
'''

import sys,logging,random,time

import liarsdice

def make_player(s) :
    filename = s
    attr = 'get_move'
    if -1 != s.find('.') :
        filename,attr = s.split('.')
    try :
        m = __import__(filename)
    except :
        logging.warn('couldn\'t import "%s"' % filename)
        return None
    f = getattr(m,attr)
    return f

def play_games(n,seed,player_names,rules) :
    random.seed(seed)
    players = {}
    scores = {}
    names = {}
    for i in player_names :
        player_id = chr(ord('A') + len(players))
        names[player_id] = i
        logging.debug('making player %s (%s) ...' % (player_id,i))
        p = make_player(i)
        players[player_id] = p
        scores[player_id] = 0
    game_num = 0
    for r in range(n) :
        game_num += 1
        logging.debug('playing game %d ...' % (game_num,))
        winner = liarsdice.play_game(players,rules)
        scores[winner] += 1
        logging.debug('RESULT\tgame:%d\twinner:%s' % (game_num,winner))
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        rank = 0
        for i in k :
            rank += 1
            logging.debug('SCORE\tgame %d of %d\t#%d.\t%s\t%s\t%d' % (game_num,n,rank,i,names[i],scores[i]))
        logging.debug('SCORE')
    return scores

def main(argv) :
    if 1 == len(argv) :
        print HELP
        sys.exit()

    c = argv[1]

    if 0 :
        pass

    elif 'help' == c :
        print HELP
        sys.exit()

    elif 'human' == c :
        logging.basicConfig(level=logging.INFO,format='%(message)s',stream=sys.stdout)
        opponent = 'players.p_simpleton'
        if 3 == len(argv) :
            opponent = sys.argv[2]
        play_games(1,time.time(),('players.p_human',opponent),liarsdice.RULES_DEFAULT)

    elif 'play' == c :
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)-7s %(message)s',stream=sys.stdout)
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        play_games(n,''.join(sys.argv),player_names,liarsdice.RULES_DEFAULT)

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

