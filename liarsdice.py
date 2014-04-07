#!/usr/bin/python

# liarsdice.py -- play liarsdice

HELP = '''\
usage:

    $ python liarsdice.py play 10 my_robot.get_play his_robot.get_play robots.dummy

Play 10 games of liar's dice between get_play() in my_robot.py, get_play in 
his_robot.py, and dummy() in robots.py.
'''

import sys,logging,os,random,time

def play_game(players) :
    
    # first, set up the players left in the game
    #
    in_game = players.keys()
    random.shuffle(in_game)
    whose_move = 0
    dice = {}
    for i in in_game :
        dice[i] = 5

    logging.info('new game between %s' % ', '.join(in_game))

    # keep playing hands until only one player left
    #
    winner = None
    while None == winner :

        for i in in_game :
            if 0 != dice[i] :
                if None != winner :
                    winner = None
                    break
                winner = i
        if None != winner :
            break

        # everyone rolls their dice
        #
        logging.info('new hand between %s' % ', '.join(filter(lambda x : 0 != dice[x],in_game)))
        hands = {}
        for i in in_game :
            if 0 == dice[i] :
                continue
            hands[i] = []
            logging.debug('rolling %d dice for "%s" ...' % (dice[i],i))
            for j in range(dice[i]) :
                hands[i].append(random.choice((1,2,3,4,5,6)))
        logging.info('hands: %s' % str(filter(lambda x : 0 != dice[x[0]],hands.items())))
        history = []
        
        # keep playing hands until someone calls liar
        #
        while 1 :
            
            # build history
            #
            history_str = ','.join(map(lambda x : '%s:%d' % (x[0],x[1]),history))

            # build hands
            #
            hands_str = '%s:%s' % (in_game[whose_move],''.join(map(lambda x : str(x),hands[in_game[whose_move]])))
            for i in in_game :
                if i != in_game[whose_move] :
                    hands_str += ',%s:%s' % (i,'.' * dice[i])

            # get the play
            #
            logging.info('getting move from "%s"' % in_game[whose_move])
            play = 0
            try :
                play = int(players[in_game[whose_move]](in_game[whose_move],hands_str,history_str))
            except :
                logging.warn('caught exception "%s" calling "%s"' % (sys.exc_info()[1],in_game[whose_move]))
            logging.info('player "%s" played "%d"' % (in_game[whose_move],play))

            # check for legal moves
            # 
            if 0 != play :
                face = play % 10
                quantity = play / 10
                if face <= 0 or face > 6 or quantity <= 0 or quantity > (len(players) * 5) :
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
            if 0 == play :
                
                # if it's the first play, they lose
                #
                if 1 == len(history) :
                    logging.debug('called liar before any plays')
                    loser = in_game[whose_move]

                else :
                    
                    # count dice
                    #
                    common_dice = [0,0,0,0,0,0]
                    for i in in_game :
                        if 0 == dice[i] :
                            continue
                        for j in hands[i] :
                            common_dice[j - 1] += 1

                    logging.debug('hands: %s' % str(hands))
                    logging.debug('common dice: %s' % str(common_dice))

                    last_play = history[-2][1]
                    last_face = last_play % 10
                    last_quantity = last_play / 10
                    if common_dice[last_face - 1] >= last_quantity :
                        logging.debug('last play valid')
                        loser = in_game[whose_move]
                    else :
                        logging.debug('last play is NOT valid')
                        loser = in_game[history[-2][0]]

                # remove loser's die, bump them if they're out of dice,
                # and start over again
                #
                logging.debug('removing a die from "%s"' % loser)
                dice[loser] -= 1
                if 0 == dice[loser] :
                    logging.debug('"%s" has no dice' % loser)
                    if loser == in_game[whose_move] :
                        logging.debug('and it\'s his move')
                        while 1 :
                            whose_move += 1
                            if whose_move == len(in_game) :
                                whose_move = 0
                            if 0 != dice[in_game[whose_move]] :
                                break
                break
                    
            # otherwise, just add it to the history and continue
            #
            else :
                while 1 :
                    whose_move += 1
                    if whose_move == len(in_game) :
                        whose_move = 0
                    if 0 != dice[in_game[whose_move]] :
                        break

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

def play_games(n,seed,player_names) :
    random.seed(seed)
    players = {}
    scores = {}
    names = {}
    for i in player_names :
        player_id = chr(ord('A') + len(players))
        names[player_id] = i
        logging.info('making player %s (%s) ...' % (player_id,i))
        p = make_player(i)
        players[player_id] = p
        scores[player_id] = 0
    game_num = 0
    for r in range(n) :
        game_num += 1
        logging.info('playing game %d ...' % (game_num,))
        winner = play_game(players)
        scores[winner] += 1
        logging.info('RESULT\tgame:%d\twinner:%s' % (game_num,winner))
        k = scores.keys()
        k.sort(key = lambda x : scores[x],reverse = True)
        for i in k :
            logging.info('SCORE\tgame %d of %d\t%s\t%s\t%d' % (game_num,n,i,names[i],scores[i]))
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

    elif 'play' == c :
        n = int(sys.argv[2])
        player_names = sys.argv[3:]
        play_games(n,''.join(sys.argv),player_names)

    else :
        logging.error('i don\'t know how to "%s". look at the source' % c)
        print HELP
        sys.exit()

if __name__ == '__main__' :
    main(sys.argv)

