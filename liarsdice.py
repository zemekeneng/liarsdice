#!/usr/bin/python

# liarsdice.py -- play liarsdice
#

HELP = '''\
usage:

    $ python liarsdice.py games 10 my_robot.get_play his_robot.get_play robots.dummy

Play 10 games of liar's dice between get_play() in my_robot.py, get_play in 
his_robot.py, and dummy() in robots.py.
'''
 
import sys,logging,os,random,time

def nyi() :
    raise NotImpementedError

class Game :

    def __init__(self) :
        self.playes = None
        
    def new_game(self,players) :
        self.players = players

    def serialize(self) :   
        nyi()

    def deserialize(self,s) :
        nyi()

    def dump(self) :
        nyi()

    def play_game(self) :
        return random.choice(self.players.keys())

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

def play_games(n,seed,player_names) :
    random.seed(seed)
    players = {}
    scores = {}
    for i in player_names :
        player_id = 'p%d__%s' % (len(players) + 1,i)
        logging.info('making player %s ...' % player_id)
        p = make_player(i)
        players[player_id] = p
        scores[player_id] = 0
    game_num = 0
    for r in range(n) :
        game_num += 1
        logging.info('playing game %d ...' % (game_num,))
        game = Game()
        game.new_game(players)
        winner = game.play_game()
        scores[winner] += 1
        logging.info('RESULT\tgame:%d\twinner:%s' % (game_num,winner))
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        for i in k :
            logging.info('SCORE\tgame %d of %d\t%s\t%d' % (game_num,n,i,scores[i]))
    return scores

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

    elif 'games' == c :
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        play_games(n,''.join(sys.argv),player_names)

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

