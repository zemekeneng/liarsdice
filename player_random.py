# player_random.py, play the first word found in dictionary

import random

g_sowpods = None
def get_random_word() :
    global g_sowpods
    if None == g_sowpods :
        g_sowpods = []
        for i in file('sowpods.txt').readlines() :
            g_sowpods.append(i[:-1])
    return random.choice(g_sowpods)

def word_in_tiles(word,tiles) :
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

def has_been_played(move,tiles,moves) :
    word = ''.join(map(lambda x : tiles[x],move))
    for i in moves :
        if None == i :
            continue
        if word == ''.join(map(lambda x : tiles[x],i[:len(word)])) :
            return True
    return False

def get_move(tiles,moves,colors) :
    for i in range(1000) :
        word = get_random_word()
        move = word_in_tiles(word,tiles)
        if None == move :
            continue
        if not has_been_played(move,tiles,moves) :
            return move
    return None

