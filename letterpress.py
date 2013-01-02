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
        
    def new_game(self,tiles,players) :
        '''
        tiles can be None, if so, we'll generate a random board
        players is a pair of (name,get_move) pairs
        '''
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
        self.players = players

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
    def generate_board(cls) :
        tiles = ''
        for i in range(25) :
            tiles += random.choice(Game.TILES_LETTER_FREQ)
        return tiles
        
    def player_display(self,i) :
        return 'player %d (%s)' % (i,self.players[i][0])

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
        canvas.append('%s: %d, %s: %d' % (self.player_display(0),len(filter(lambda x : x == 1,self.colors)),self.player_display(1),len(filter(lambda x : x == 2,self.colors))))
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

    def play_game(self) :

        logging.info('tiles: %s' % self.tiles)

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
                move = self.players[whose_move][1](self.tiles[:],self.moves[:],self.colors[:])
                logging.info("move: %s" % str(move))
            else :
                try :
                    move = self.players[whose_move][1](self.tiles[:],self.moves[:],self.colors[:])
                    logging.info("move: %s" % str(move))
                except :
                    logging.info('%s threw an exception ("%s"), disqualifying ...' % (self.player_display(whose_move),str(sys.exc_info()[:2])))
                    disqualified = whose_move
                    break

            # did they take too long?
            #
            elapsed = time.time() - started
            self.clocks[whose_move] += elapsed
            if Game.MAX_TIME_PER_GAME < self.clocks[whose_move] :
                logging.info('%s took too long, disqualifying ...' % (self,player_display(whose_move),))
                if not self.debug :
                    disqualified = whose_move
                break

            # legal move?
            #
            legal = self.is_legal_move(move)
            if not legal[0] :
                logging.info('%s played illegal move (%d, %s), disqualifying ...' % (self.player_display(whose_move),legal[1],legal[2]))
                disqualified = whose_move
                break

            # looks good, let's play it
            #
            logging.info('%s played %s ...' % (self.player_display(whose_move),str(move)))
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
            logging.info('%s wins' % self.player_display(winner - 1))
            return winner

        # nope, let's count colors
        #
        winner = self.get_winner()
           
        # all done, return result
        #
        if 0 == winner  :
            logging.info('game over, tie game')
        else :
            logging.info('game over, %s wins' % self.player_display(winner - 1))
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
    random.seed(seed)
    players = {}
    scores = {}
    for i in player_names :
        player_id = 'p%d__%s' % (len(players) + 1,i)
        logging.info('making player %s ...' % player_id)
        p = make_player(i)
        players[player_id] = p
        scores[player_id] = 0
    logging.info('generating game boards ...')
    game_boards = []
    for i in range(n) :
        game_boards.append(Game.generate_board())
    results = {}
    game_num = 0
    for r in range(n) :
        for p1 in players.keys() :
            for p2 in players.keys() :
                if p1 == p2 :
                    continue
                game_num += 1
                logging.info('playing game %d between %s (player 1) and %s (player 2) on game board %s ...' % (game_num,p1,p2,game_boards[r]))
                game = Game()
                game.new_game(game_boards[r],((p1,players[p1]),(p2,players[p2])))
                result = game.play_game()
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
                logging.info('RESULT\t%d, %d\t%s\t%s\t%s\t%d' % (game_num,r,p1,p2,game_boards[r],result))
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        for i in k :
            logging.info('SCORE\tround %d of %d\t%s\t%d' % (r + 1,n,i,scores[i]))
        logging.info('SCORE')
    return results

def single_game(player_name_1,player_name_2,tiles = None) :
    logging.info('making player %s ...' % player_name_1)
    p1 = make_player(player_name_1)
    logging.info('making player %s ...' % player_name_2)
    p2 = make_player(player_name_2)
    logging.info('playing game between %s (player 1) and %s (player 2) ...' % (player_name_1,player_name_2))
    game = Game()
    game.new_game(tiles,((player_name_1,p1),(player_name_2,p2)))
    game.debug = True
    result = game.play_game()
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

