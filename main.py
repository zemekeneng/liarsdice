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

    To run a tournament with the above with seed "frog":
        
        $ python main.py tournament frog 10 my_robot.get_play his_robot.get_play robots.dummy

'''

import sys,logging,random,time

import liarsdice

def make_player(s,catch_exceptions) :
    filename = s
    attr = 'get_move'
    if -1 != s.find('.') :
        filename,attr = s.split('.')
    try :
        m = __import__(filename)
    except e :
        if not catch_exceptions :
            raise
        logging.warn('couldn\'t import "%s"' % filename)
        return None
    f = getattr(m,attr)
    return f

def play_games(n,seed,player_names,catch_exceptions) :
    random.seed(seed)
    players = {}
    scores = {}
    names = {}
    for i in player_names :
        player_id = chr(ord('A') + len(players))
        names[player_id] = i
        logging.info('making player %s (%s) ...' % (player_id,i))
        p = make_player(i,catch_exceptions)
        players[player_id] = p
        scores[player_id] = 0
    game_num = 0
    for r in range(n) :
        game_num += 1
        logging.debug('playing game %d ...' % (game_num,))
        winner = liarsdice.play_game(players,catch_exceptions)
        scores[winner] += 1
        logging.debug('RESULT\tgame:%d\twinner:%s' % (game_num,winner))
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        rank = 0
        for i in k :
            rank += 1
            logging.info('SCORE\tgame %d of %d\t#%d.\t%s\t%s\t%d' % (game_num,n,rank,i,names[i],scores[i]))
        logging.info('SCORE')
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
        play_games(1,time.time(),('players.p_human',opponent),False)

    elif 'play' == c :
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)-7s %(message)s',stream=sys.stdout)
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        play_games(n,''.join(player_names),player_names,False)
  
    elif 'tournament' == c :
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)-7s %(message)s',stream=sys.stdout)
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        play_games(n,''.join(player_names),player_names,True)
    
    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

