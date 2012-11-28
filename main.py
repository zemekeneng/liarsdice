#!/usr/bin/python

# play letterpress
#
#   https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8
#

import sys,logging,os,random,time

def help() :
    logging.error('''\
meh, look at the source. 

or try:

    % python letterpress.py game foo foo

(this plays a game between foo.py and foo.py)
''')

class Ref :
    
    def __init__(self,rng,player_1,player_2) :
        self.rng = rng
        self.player_1 = player_1
        self.player_2 = player_2

    def play_game(self) :
        # TODO: implement
        return self.rng.choice((0,1,2))

def make_player(s) :
    try :
        m = __import__(s)
    except :
        logging.warn('couldn\'t import "%s"' % s)
        return None
    f = getattr(m,'get_play')
    return f
    
def main(argv) :

    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',stream=sys.stdout)
    if 0 == len(argv) :
        help()
        sys.exit()

    c = argv[1]

    if 0 :
        pass

    elif 'help' == c :
        help()
        sys.exit()

    elif 'game' == c :
        seed = ""
        if 5 == len(argv) :
            seed = argv[4]
        if 0 == len(seed) :
            seed = int(time.time() * 100)
        logging.info('making player "%s" as player 1 ...' % argv[2])
        p1 = make_player(argv[2])
        logging.info('making player "%s" as player 2 ...' % argv[3])
        p2 = make_player(argv[3])
        logging.info('setting up random number generator with seed "%s" ...' % seed)
        rng = random.Random(seed)
        logging.info('creating referree ...')
        ref = Ref(rng,p1,p2)
        logging.info('playing game ...')
        r = ref.play_game()
        logging.info('RESULT\t%d' % r)
        sys.exit()

    elif 'games' == c :
        n = int(argv[2])
        seed = argv[3]
        if 0 == len(seed) :
            seed = int(time.time() * 100)
        p1 = make_player(argv[4])
        p2 = make_player(argv[5])
        rng = random.Random(seed)
        ref = Ref(rng,p1,p2)
        results = {}
        for i in range(n) :
            r = ref.play_game()
            if not results.has_key(r) :
                results[r] = 0
            results[r] += 1
        for i,j in results.items() :
            logging.info('RESULT\t%s\t%d' % (i,j))

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        help()
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

