# threes.py -- a dumb letterpress algo, always plays common three letter words

COMMON_THREE_LETTER_WORDS = [
    'all', 'and', 'any', 'are', 'boy', 'but', 'can', 'dad', 'day', 
    'did', 'for', 'get', 'has', 'her', 'him', 'his', 'how', 'its', 
    'let', 'man', 'mom', 'new', 'not', 'now', 'old', 'one', 'our', 
    'out', 'put', 'say', 'see', 'she', 'the', 'too', 'two', 'use', 
    'was', 'way', 'who', 'you', 
    'xxx' # deliberate word not in sowpods
]

import random

def get_play(tiles,colors,moves) :
    '''
    return a random three letter word if it can find it. sometimes returns None,
    sometimes returns a word not in sowpods, sometimes returns an unplayable word
    (eg, 'all' with only one l on board)
    '''
    for i in range(25 * 25 * 25) :
        p = (random.randint(0,24),random.randint(0,24),random.randint(0,24))
        if ''.join(map(lambda x : tiles[x],p)) in COMMON_THREE_LETTER_WORDS :
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
