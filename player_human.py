# player_human.py, play against the computer

def dump_game(tiles,moves,colors) :
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

def find_moves(word,tiles) :
    indexes = {}
    for z in range(25) :
        i = tiles[z]
        if not indexes.has_key(i) :
            indexes[i] = []
        indexes[i].append(z)

    def find_moves_helper(indexes,sofar,whatsleft) :
        if 0 == len(whatsleft) :
            return [sofar,]
        letter = whatsleft[0]
        moves = []
        for i in indexes.get(letter,[]) :
            if i in sofar :
                continue
            nextsofar = sofar[:]
            nextsofar.append(i)
            x = find_moves_helper(indexes,nextsofar,whatsleft[1:])
            if 0 == len(x) :
                return []
            moves.extend(x)
        return moves

    return find_moves_helper(indexes,[],word)

def get_move(tiles,moves,colors) :
    while 1 :
        dump_game(tiles,moves,colors)
        print 'You are player #%d. What is your word? ' % (len(moves) % 2 + 1,)
        word = raw_input()
        a = find_moves(word,tiles)
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

