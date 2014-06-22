# ben_player.py -- sample liar's dice robot

import random, logging, operator as op
import numpy as np

def nCr(n,r):
    r = min(r, n-r)
    if r == 0: return 1.0
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

def determine_next_bid(last_bid, my_hand, uk_dice, players):
    hand = parse_hand(my_hand)
    candidates = find_candidates(last_bid)
    can_probs = {x: naive_odds(uk_dice, hand[x%10], x//10) for x in candidates}
    if last_bid >= 11:
        for bid in can_probs:
            if bid%10 == last_bid%10:
                can_probs[bid] = can_probs[bid] * 1
        can_probs[0] = 1.0 - naive_odds(uk_dice, hand[last_bid%10], last_bid//10)
    my_prob = max(can_probs.iteritems(), key=op.itemgetter(1))
    return my_prob[0]

def p_history(history):
    if 0 == len(history) :
        return 10
    else :
        return int(history.split(',')[-1].split(':')[1])

class Record(object):
    def __init__(self):
        self.record = []
        self.dataset = []
        self.ld = 0
        self.games = 0

    def record_play(self, me, hands, history):
        # split and parse hands for each player
        hands = {h[0]:parse_hand(h[1]) \
                        for h in [hand.split(':') \
                           for hand in hands.split(',')]}
        # total dice in play                   
        d = sum([sum(hands[hand].itervalues()) for hand in hands])

        # split the player, the face, and the naive odds of a bid
        phistory = []
        for bid in history.split(','):
            phistory.append(bid.split(':'))
        history = [[bid[0],
            int(bid[1])%10,
            1 - odds(d,int(bid[1])//10)] for bid in phistory if int(bid[1]) != 0]
        players_highest_bid = {h:{int(x):0 for x in '123456'} for h in hands.keys()}
        data = []
        print history
        for h in history:
            players_highest_bid[h[0]][h[1]] = h[2]
            data.append([h[0], players_highest_bid[h[0]].copy()])
            print data

        self.record.append([hands, history])
        self.dataset.append([hands, data])
        if self.games == 100:
            print np.array(self.dataset)

def get_play(me,hands,history) :
    
    if not hasattr(get_play, "r"):
        get_play.r = Record()

    last_bid = p_history(history)


    if 0 == last_bid :
        get_play.r.record_play(me, hands, history)
        return 0
    
    num_dice = sum(map(lambda x : len(x.split(':')[1]),hands.split(',')))
 
    my_hand = None
    players_dice = {}
    for i in hands.split(',') :
        who,dice = i.split(':')
        players_dice[who] = len(dice)
        if who == me :
            my_hand = dice

    if get_play.r.ld < num_dice:
        get_play.r.games += 1
    get_play.r.ld = num_dice

    return determine_next_bid(
                              last_bid,
                              my_hand,
                              num_dice - len(my_hand),
                              len(players_dice)
                              )


def main():
    print odds(0,1)

if __name__ == '__main__':
    main()