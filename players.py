# players.py -- some sample players

# included players:
#
#   p_top_left        -- always play the top left -most 3 tiles
#   p_all_twos        -- looks for any two letter word
#   p_common_threes   -- looks for common three letter words
#   p_random          -- play a random word in sowpods
#   p_human           -- play against human on the console

import random

def p_top_left(tiles,moves,colors) :
    
    return (0,1,2)

ALL_TWO_LETTER_WORDS = [
'aa', 'ab', 'ad', 'ae', 'ag', 'ah', 'ai', 'al', 'am', 'an', 'ar', 'as', 
'at', 'aw', 'ax', 'ay', 'ba', 'be', 'bi', 'bo', 'by', 'ch', 'da', 'de', 
'di', 'do', 'ea', 'ed', 'ee', 'ef', 'eh', 'el', 'em', 'en', 'er', 'es', 
'et', 'ex', 'fa', 'fe', 'fy', 'gi', 'go', 'gu', 'ha', 'he', 'hi', 'hm', 
'ho', 'id', 'if', 'in', 'io', 'is', 'it', 'ja', 'jo', 'ka', 'ki', 'ko', 
'ky', 'la', 'li', 'lo', 'ma', 'me', 'mi', 'mm', 'mo', 'mu', 'my', 'na', 
'ne', 'no', 'nu', 'ny', 'ob', 'od', 'oe', 'of', 'oh', 'oi', 'om', 'on', 
'oo', 'op', 'or', 'os', 'ou', 'ow', 'ox', 'oy', 'pa', 'pe', 'pi', 'po', 
'qi', 're', 'sh', 'si', 'so', 'st', 'ta', 'te', 'ti', 'to', 'ug', 'uh', 
'um', 'un', 'up', 'ur', 'us', 'ut', 'we', 'wo', 'xi', 'xu', 'ya', 'ye', 
'yo', 'yu', 'za', 'zo', 'zz',
]

def p_all_twos(tiles,colors,moves) :
    '''
    return a random two letter word if it can find it. sometimes returns None,
    sometimes returns an unplayable word
    (eg, 'aa' with only one 'a' on board)
    '''
    for i in range(25 * 25) :
        p = (random.randint(0,24),random.randint(0,24),)
        if p[0] == p[1] :
            continue
        if ''.join(map(lambda x : tiles[x],p)) in ALL_TWO_LETTER_WORDS :
            return p
    return None

COMMON_THREE_LETTER_WORDS = [
    'all', 'and', 'any', 'are', 'boy', 'but', 'can', 'dad', 'day', 
    'did', 'for', 'get', 'has', 'her', 'him', 'his', 'how', 'its', 
    'let', 'man', 'mom', 'new', 'not', 'now', 'old', 'one', 'our', 
    'out', 'put', 'say', 'see', 'she', 'the', 'too', 'two', 'use', 
    'was', 'way', 'who', 'you', 
]

def p_common_threes(tiles,colors,moves) :
    '''
    return a random three letter word if it can find it. sometimes returns None,
    sometimes returns a word not in sowpods, sometimes returns an unplayable word
    (eg, 'all' with only one l on board)
    '''
    for i in range(25 * 25 * 25) :
        p = (random.randint(0,24),random.randint(0,24),random.randint(0,24))
        if p[0] == p[1] or p[1] == p[2] or p[0] == p[2] :
            continue
        if ''.join(map(lambda x : tiles[x],p)) in COMMON_THREE_LETTER_WORDS :
            return p
    return None

g_sowpods = None
def _get_random_word() :
    global g_sowpods
    if None == g_sowpods :
        g_sowpods = []
        for i in file('sowpods.txt').readlines() :
            g_sowpods.append(i[:-1])
    return random.choice(g_sowpods)

def _word_in_tiles(word,tiles) :
    m = []
    for i in word :
        indexes = []
        z = 0
        while 1 :
            z = tiles.find(i,z)
            if -1 == z :
                break
            if not z in m :
                indexes.append(z)
            z += 1
        if 0 == len(indexes) :
            return None
        m.append(random.choice(indexes))
    return m 

def _has_been_played(move,tiles,moves) :
    word = ''.join(map(lambda x : tiles[x],move))
    for i in moves :
        if None == i :
            continue
        if word == ''.join(map(lambda x : tiles[x],i[:len(word)])) :
            return True
    return False

def p_random(tiles,moves,colors) :
    for i in range(1000) :
        word = _get_random_word()
        move = _word_in_tiles(word,tiles)
        if None == move :
            continue
        if not _has_been_played(move,tiles,moves) :
            return move
    return None

def _dump_game(tiles,moves,colors) :
    canvas = []
    for y in range(5) :
        board_pic = ''
        colors_pic = ''
        for x in range(5) :
            z = (y * 5) + x
            board_pic += tiles[z]
            colors_pic += '.12'[colors[z]]
        canvas.append(board_pic + ' ' + colors_pic)
    for i in canvas :
        print i
    m = []
    for i in moves :
        if None == i :
            m.append('PASS')
        else :
            m.append(''.join(map(lambda x : tiles[x],i)))
    t = ', '.join(m)
    print t

def _find_moves(word,tiles) :
    indexes = {}
    for z in range(25) :
        i = tiles[z]
        if not indexes.has_key(i) :
            indexes[i] = []
        indexes[i].append(z)

    def _find_moves_helper(indexes,sofar,whatsleft) :
        if 0 == len(whatsleft) :
            return [sofar,]
        letter = whatsleft[0]
        moves = []
        for i in indexes.get(letter,[]) :
            if i in sofar :
                continue
            nextsofar = sofar[:]
            nextsofar.append(i)
            x = _find_moves_helper(indexes,nextsofar,whatsleft[1:])
            if 0 == len(x) :
                return []
            moves.extend(x)
        return moves

    return _find_moves_helper(indexes,[],word)

def p_human(tiles,moves,colors) :
    while 1 :
        _dump_game(tiles,moves,colors)
        print 'You are player #%d. What is your word? ' % (len(moves) % 2 + 1,)
        word = raw_input()
        a = _find_moves(word,tiles)
        if 1 == len(a) :
            return a[0]
        if 0 == len(a) :
            continue
        print 'There are multiple ways to make "%s". Please choose one.' % word
        for i in range(len(a)) :
            print '%5d) %s' % (i + 1,' '.join(map(lambda x : '%d,%d' % ((x % 5) + 1,(x / 5) + 1),a[i])))
        choice = raw_input()
        try :
            x = int(choice) - 1
        except :
            continue
        if x < 0 or x >= len(a) :
            continue
        return a[x]

