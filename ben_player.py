# ben_player.py -- sample liar's dice robot

import random, logging, operator as op

def nCr(n,r):
    r = min(r, n-r)
    if r == 0: return 1
    try:
        numer = reduce(op.mul, xrange(n, n-r, -1))
        denom = reduce(op.mul, xrange(1, r+1))
    except:
        numer, denom = 1, 1
    return float(numer//denom)

def exact_odds(n,q):
    """for a given number of unknown dice n, the probability that
    exactly a certain quantity q of any face value are showing"""
    return float(nCr(n,q) * (1.0/6)**q * (5.0/6)**(n-q))

def odds(n,x):
    "the odds of an x face roll give n unknown dice"
    return sum([exact_odds(n,x) for x in range(x,n+1)])

def naive_odds(uk_dice, my_faces, bet):
    if bet <= my_faces:
        return 1.0
    else:
        return odds(uk_dice, bet - my_faces)

def parse_hand(raw_hand):
    hand = {int(n):0 for n in '123456'}
    for face in raw_hand:
        hand[int(face)] += 1
    return hand

def find_candidates(last_bid):
    candidates = []
    for x in range(1,6+1):
        if last_bid % 10 < 6:
            last_bid += 1
            candidates.append(last_bid)
        else:
            last_bid = (last_bid // 10) * 10 + 11
            candidates.append(last_bid)
    return candidates

def determine_next_bid(last_bid, my_hand, uk_dice):
    hand = parse_hand(my_hand)
    candidates = find_candidates(last_bid)
    can_probs = {x: naive_odds(uk_dice, hand[x%10], x//10) for x in candidates}
    if last_bid >= 11:
        can_probs[0] = 1.0 - naive_odds(uk_dice, hand[last_bid%10], last_bid//10)
    print can_probs
    return max(can_probs.iteritems(), key=op.itemgetter(1))[0]

def p_history(history):
    if 0 == len(history) :
        return 10
    else :
        return int(history.split(',')[-1].split(':')[1])

def get_play(me,hands,history) :
    
    # figure out the previous call
    #
    last_bid = p_history(history)

    # showdown? if so, just ignore
    #
    if 0 == last_bid :
        return 0
    
    # count the total number of dice
    #
    num_dice = sum(map(lambda x : len(x.split(':')[1]),hands.split(',')))
 
    # find my hand
    #
    my_hand = None
    for i in hands.split(',') :
        who,dice = i.split(':')
        if who == me :
            my_hand = dice
            break

    # try 4 times to find pick
    # a random better play, if
    # can't, just call
    #
    return determine_next_bid(last_bid, my_hand, num_dice - len(my_hand))

    # nothing found, just call
    # 
    logging.debug('nothing found, calling ...')
    return 0

def main():
    print nCr(0,1)

if __name__ == '__main__':
    main()