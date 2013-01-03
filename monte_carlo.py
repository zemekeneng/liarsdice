import random

BOT_A       = 7.0       # "strength" of bot A (sides of die)
BOT_B       = 6.0       # "strength" of bot B (sides of die)
N           = 100       # number of games in tournament
SIM         = 1000      # number of simulations to run
CONFIDENCE  = 0.9       # confidence level we're testing

def test() :
    x_a = random.random() * BOT_A
    x_b = random.random() * BOT_B
    return x_a > x_b

def tournament() :
    wins_a = 0
    wins_b = 0
    for i in range(N) :
        x = test()
        if x :
            wins_a += 1
        else :
            wins_b += 1
    return (wins_a,wins_b)

def monte_carlo() :
    success = 0
    for i in range(SIM) :
        wins_a,wins_b = tournament()
        if wins_a > wins_b :
            success += 1
    return success

success = monte_carlo()
if (success / float(SIM)) > CONFIDENCE :
    can_or_cannot = 'CAN'
else :
    can_or_cannot = 'CANNOT'

print '''
I simulated %(SIM)d %(N)d-game tournaments between bot A 
with strength %(BOT_A).2f against bot B with strength %(BOT_B).2f.
%(success)d times out of %(SIM)d, bot A beat bot B.
Therefore, I %(can_or_cannot)s say with %(CONFIDENCE).2f confidence 
that bot A is better than bot B.
''' % globals()

