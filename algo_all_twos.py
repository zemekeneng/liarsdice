# algo_all_twos.py -- a dumb letterpress algo, always plays a two letter word

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
'bb', # deliberate bad word
]

import random

def get_move(tiles,colors,moves) :
    '''
    return a random two letter word if it can find it. sometimes returns None,
    sometimes returns an unplayable word
    (eg, 'aa' with only one 'a' on board)
    '''
    for i in range(25 * 25) :
        p = (random.randint(0,24),random.randint(0,24),)
        if ''.join(map(lambda x : tiles[x],p)) in ALL_TWO_LETTER_WORDS :
            return p
    return None

if __name__ == '__main__' :
    for i in range(1000) :
        t = ''
        for j in range(25) :
            t += random.choice('abcdefghijklmnopqrstuvwxyz')
        p = get_play(t,None,None)
        if None == p :
            w = None
        else :
            w = ''.join(map(lambda x : t[x],p))
        print '%s\t%s\t%s' % (t,p,w)
