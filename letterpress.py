#!/usr/bin/python

# letterpress.py -- play letterpress
#
#   https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8
#

HELP = '''\
letterpress.py -- this program pits letterpress players against each other

Play a game between player_random.py and player_human.py:

    % python letterpress.py game player_random player_human

Play 100 round robin games between player_123.py, player_common_threes.py, and 
player_my_algo, using seed "seed":

    % python letterpress.py tournament 100 seed player_123 player_common_threes player_my_algo

See player_test.py for documentation on how to write a player.
'''

import sys,logging,os,random,time,cPickle

g_sowpods = None

class Game :

    # maximum allowed time per game per player
    #
    MAX_TIME_PER_GAME = 60

    # this distribution is calculated from the square root of the observed frequency in sowpods
    #
    TILES_LETTER_FREQ = 'aaaaaabbbccccddddeeeeeeeeffgggghhhiiiiiiijkklllllmmmmnnnnnnooooooppppqrrrrrrsssssssttttttuuuuvvwwxyyyz'

    def __init__(self) :
        pass
        
    def new_game(self,tiles = None) :
        self.moves = []
        self.colors = []
        for i in range(25) :
            self.colors.append(0)
        self.clocks = [0.0,0.0]
        if None == tiles :
            self.tiles = self.generate_board()
        else :
            self.tiles = tiles
        self.debug = False

    def serialize(self) :   
        return cPickle.dumps((self.tiles,self.moves,self.colors))

    def deserialize(self,s) :
        self.tiles,self.moves,self.colors = cPickle.loads(s)

    @classmethod
    def word_in_sowpods(cls,word) :
        global g_sowpods
        if None == g_sowpods :
            g_sowpods = {}
            for i in file('sowpods.txt').readlines() :
                g_sowpods[i[:-1]] = 1
        return word in g_sowpods

    @classmethod
    def generate_board(cls,rng = None) :
        if None == rng :
            rng = random.Random()
        tiles = ''
        for i in range(25) :
            tiles += rng.choice(Game.TILES_LETTER_FREQ)
        return tiles
        
    def dump(self) :
        canvas = []
        for y in range(5) :
            board_pic = ''
            colors_pic = ''
            for x in range(5) :
                z = (y * 5) + x
                board_pic += self.tiles[z]
                colors_pic += '.12'[self.colors[z]]
            canvas.append(board_pic + ' ' + colors_pic)
        m = []
        for i in self.moves :
            if None == i :
                m.append('PASS')
            else :
                m.append('%s (%s)' % (''.join(map(lambda x : self.tiles[x],i)),i))
        t = ', '.join(m)
        canvas.append(t)
        canvas.append('player 1: %d, player 2: %d' % (len(filter(lambda x : x == 1,self.colors)),len(filter(lambda x : x == 2,self.colors))))
        return canvas

    def is_legal_move(self,move) :

        # always ok to pass
        #
        if None == move :
            return (True,)

        # they played a word, make sure it is a legal play
        #
        word = ''
        try :
            move = tuple(move)
            used = {}
            for i in move :
                if i in used :
                    return (False,1,'used same tile twice')
                used[i] = 1
                word += self.tiles[i]
        except :
            return (False,2,'bad syntax')

        # in dictionary?
        #
        if not self.word_in_sowpods(word) :
            return (False,3,'"%s" not in dictionary' % word)

        # already been played?
        #
        word = ''.join(map(lambda x : self.tiles[x],move))
        for i in self.moves :
            if None == i :
                continue
            if ''.join(map(lambda x : self.tiles[x],i[:len(word)])) == word :
                return (False,4,'already played')

        # looks good
        #
        return (True,)

    def is_game_over(self) :

        # two consecutive passes?
        #
        if 2 <= len(self.moves) and None == self.moves[-1] and None == self.moves[-2] :
            return True
        
        # all tiles colored?
        #
        if 25 == len(filter(lambda x : x != 0,self.colors)) :
            return True

        # nope.
        #
        return False

    def do_move(self,move) :

        # remember the move
        #
        self.moves.append(move)

        # pass?
        #
        if None == move :
            return

        # update the colors
        #
        new_colors = []
        color = ((len(self.moves) - 1) % 2) + 1
        for i in move :
            
            # make sure it isn't surrounded
            #
            surrounded = True
            x = i % 5 
            y = i / 5
            if surrounded and x > 0 and self.colors[i - 1] in (0,color) :
                surrounded = False
            if surrounded and x < 4 and self.colors[i + 1] in (0,color) :
                surrounded = False
            if surrounded and y > 0 and self.colors[i - 5] in (0,color) :
                surrounded = False
            if surrounded and y < 4 and self.colors[i + 5] in (0,color) :
                surrounded = False

            if self.colors[i] == 0 or not surrounded :
                new_colors.append(i)

        for i in new_colors :
            self.colors[i] = color

        return

    def get_winner(self) :
        player_1 = len(filter(lambda x : x == 1,self.colors))
        player_2 = len(filter(lambda x : x == 2,self.colors))
        if player_1 > player_2 :
            return 1
        if player_2 > player_1 :
            return 2
        return 0

    def play_game(self,player1,player2) :

        logging.info('tiles: %s' % self.tiles)
        players = (player1,player2)

        # keep playing until someone makes an illegal move,
        # or the last two moves were passes
        #
        disqualified = None
        while not self.is_game_over() :
        
            whose_move = len(self.moves) % 2
            for i in self.dump() :
                logging.debug(i)
            
            # get the player's move
            #
            started = time.time()
            if self.debug :
                move = players[whose_move](self.tiles[:],self.moves[:],self.colors[:])
                logging.info("move: %s" % str(move))
            else :
                try :
                    move = players[whose_move](self.tiles[:],self.moves[:],self.colors[:])
                    logging.info("move: %s" % str(move))
                except :
                    logging.info('player %d threw an exception ("%s"), disqualifying ...' % (whose_move + 1,str(sys.exc_info()[:2])))
                    disqualified = whose_move
                    break

            # did they take too long?
            #
            elapsed = time.time() - started
            self.clocks[whose_move] += elapsed
            if Game.MAX_TIME_PER_GAME < self.clocks[whose_move] :
                logging.info('player %d took too long, disqualifying ...' % (whose_move + 1,))
                if not self.debug :
                    disqualified = whose_move
                break

            # legal move?
            #
            legal = self.is_legal_move(move)
            if not legal[0] :
                logging.info('player %d played illegal move (%d, %s), disqualifying ...' % (whose_move + 1,legal[1],legal[2]))
                disqualified = whose_move
                break

            # looks good, let's play it
            #
            logging.info('player %d played %s ...' % (whose_move + 1,str(move)))
            self.do_move(move)

            # repeat!
            #
            continue
            
        for i in self.dump() :
            logging.debug(i)

        # did someone get disqualified?
        #
        if None != disqualified :
            winner = 2 - disqualified
            logging.info('player %d wins' % winner)
            return winner

        # nope, let's count colors
        #
        winner = self.get_winner()
           
        # all done, return result
        #
        if 0 == winner  :
            logging.info('game over, tie game')
        else :
            logging.info('game over, player %d wins' % winner)
        return winner

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

def tournament(n,seed,player_names) :
    rng = random.Random(seed)
    players = {}
    for i in player_names :
        player_id = 'p%d__%s' % (len(players) + 1,i)
        logging.info('making player %s ...' % player_id)
        p = make_player(i)
        players[player_id] = p
    logging.info('generating game boards ...')
    game_boards = []
    for i in range(n) :
        game_boards.append(Game.generate_board(rng))
    results = {}
    scores = {}
    for r in range(n) :
        for p1 in players.keys() :
            for p2 in players.keys() :
                if p1 == p2 :
                    continue
                logging.info('playing game %d between %s (player 1) and %s (player 2) on game board %s ...' % (r,p1,p2,game_boards[r]))
                game = Game()
                game.new_game(game_boards[r])
                result = game.play_game(players[p1],players[p2])
                if not results.has_key((p1,p2)) :
                    results[(p1,p2)] = []
                results[(p1,p2)].append(result)
                winner = None
                if 1 == result :
                    winner = p1
                if 2 == result :
                    winner = p2
                if not scores.has_key(winner) :
                    scores[winner] = 0
                scores[winner] += 1
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        for i in k :
            logging.info('SCORE\tround: %d of %d\t%s\t%d' % (r + 1,n,i,scores[i]))
        logging.info('SCORE')
    return results

def single_game(player_name_1,player_name_2,tiles = None) :
    logging.info('making player %s ...' % player_name_1)
    p1 = make_player(player_name_1)
    logging.info('making player %s ...' % player_name_2)
    p2 = make_player(player_name_2)
    logging.info('playing game between %s (player 1) and %s (player 2) ...' % (player_name_1,player_name_2))
    game = Game()
    game.new_game(tiles)
    game.debug = True
    result = game.play_game(p1,p2)
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
        tiles = None
        if 5 == len(sys.argv) :
            tiles = sys.argv[4]
        single_game(sys.argv[2],sys.argv[3],tiles)

    elif 'tournament' == c :
        tournament(int(sys.argv[2]),sys.argv[3],sys.argv[4:])

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

