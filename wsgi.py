#!/usr/bin/python

import sys,logging,os,random,time,cgi,urllib,wsgiref,wsgiref.simple_server,base64

import letterpress

g_players = {}

def get_player(player_name) :
    global g_players
    if '_human' == player_name :
        return None
    if not g_players.has_key(player_name) :
        g_players[player_name] = letterpress.make_player(player_name)
    return g_players[player_name]

def wsgi_response(params) :
    game = None
    if params.has_key('game') :
        game = letterpress.Game()
        game.deserialize(base64.b64decode(params.get('game')))
        players = (params.get('p1','player_random'),params.get('p2','_human'))
    if None == game or params.has_key('new_game') :
        game = letterpress.Game()
        game.new_game()
        players = (params.get('p2','player_random'),params.get('p1','_human'))

    move = params.get('move',None)
    
    d = {}
    
    d['message'] = ''
    d['button'] = '<input type=submit>'

    while 1 :
        player = players[len(game.moves) % 2]

        if '_human' == player :
            if None != move :
                try :
                    move = map(lambda x : (ord(x[0]) - ord('A')) + (5 * (ord(x[1]) - ord('1'))),filter(lambda x : -1 != '12345ABCDE '.find(x),move).split())
                except :
                    d['message'] = '<p>Bad move syntax.</p>'
                    move = None
                    break
        else :
            move = get_player(player)(game.tiles,game.moves,game.colors)
        legal = game.is_legal_move(move)
        if not legal[0] :
            d['message'] = '<p>Illegal move (%s).</p>' % legal[2]
            break
        else :
            game.do_move(move)

            if game.is_game_over() :
                winner = game.get_winner()
                if 0 == winner :
                    d['message'] = '<p>Game over. Tie. <a href="?">Play again.</p>'
                else :
                    d['message'] = '<p>Game over. %s wins.</p> <a href="?">Play again.</p>' % {1:'Red',2:'Blue'}[winner]
                d['button'] = ''
                break

            if '_human' == players[len(game.moves) % 2] :
                break

    d['red_score'] = len(filter(lambda x : x == 1,game.colors))
    d['blue_score'] = len(filter(lambda x : x == 2,game.colors))
    d['p1'] = players[0]
    d['p2'] = players[1]
    d['game'] = base64.b64encode(game.serialize())
    moves = ''
    for i in range(len(game.moves)) :
        if 0 != len(moves) :
            moves += ', ' 
        move = game.moves[i]
        moves += '<b><span style="background: %s">&nbsp;' % {1:'LightPink',2:'PowderBlue'}[(i % 2) + 1]
        if None == move :
            moves += 'PASS'
        else :
            moves += ''.join(map(lambda x : game.tiles[x],move))
        moves += '&nbsp;</span></b>'
    d['moves'] = moves

    board = []
    board.append('<table><tr><td>&nbsp;</td>')
    for i in 'ABCDE' :
        board.append('<td align=center>&nbsp;%s&nbsp;</td>' % i)
    board.append('</tr>')
    for y in range(5) :
        board.append('<tr><td align=center>%d</td>' % (y + 1))
        for x in range(5) :
            z = (y * 5) + x
            c = game.colors[z]
            surrounded = (
                ((x == 0) or (game.colors[(5 * y) + (x - 1)] == c)) and 
                ((x == 4) or (game.colors[(5 * y) + (x + 1)] == c)) and 
                ((y == 0) or (game.colors[(5 * (y - 1)) + x] == c)) and 
                ((y == 4) or (game.colors[(5 * (y + 1)) + x] == c))) 
            if 0 == c :
                color = 'white'
            elif 1 == c :
                if surrounded :
                    color = 'HotPink'
                else :
                    color = 'LightPink'
            elif 2 == c :
                if surrounded :
                    color = 'Blue'
                else :
                    color = 'LightBlue'
            board.append('<td bgcolor=%(color)s align=center><a href="#" onclick="document.getElementById(\'move\').value += \'%(tile)s (%(x)s%(y)s)  \'; document.getElementById(\'word\').value += \'%(tile)s\';">&nbsp;%(tile)s&nbsp;</a></td>' % {'color':color,'z':z,'tile':game.tiles[z],'x':chr(ord('A') + x),'y':chr(ord('1') + y)})
        board.append('</tr>')
    board.append('</table>')
    d['board'] = '\n'.join(board)

    response = '''\
<html><head><title>letterpress</title></head><body>
<h1>letterpress</h1>
%(message)s
<p>%(moves)s</p>
<p><span style="background: LightPink">&nbsp;%(red_score)d&nbsp;</span>&nbsp;&nbsp;<span style="background: LightBlue">&nbsp;%(blue_score)d&nbsp;</span></p>
<div>%(board)s</div>
<p><input type=text disabled id=word>&nbsp;&nbsp;<i><a href="#" onclick="document.getElementById('word').value='';document.getElementById('move').value='';">reset</a></i></p>
<div>
<form method=post>
<input type=hidden name=game value="%(game)s">
<input type=hidden name=p1 value="%(p1)s">
<input type=hidden name=p2 value="%(p2)s">
<input id=move type=hidden name=move value="">
%(button)s
</form>
</div>
<p>How to play:</p>
<ul>
<li>form words by clicking on tiles</li>
<li>you can't use a tile twice in a single play</li>
<li>you can't play a word that starts with a word that has been played before</li>
<li>tiles played change to your color if not surrounded by your opponent</li>
<li>game is over when all tiles are colored</li>
</ul>
<p>See <a href="https://itunes.apple.com/us/app/letterpress-word-game/id526619424?mt=8">the real letterpress game on iTunes</a>.</p>
<hr><p><a href="http://github.com/colinmsaunders/letterpress">http://github.com/colinmsaunders/letterpress</a></p>
</body></html>
''' % d

    return response

def wsgi(env,start_response) :
    params = {}
    if 'POST' == env['REQUEST_METHOD'] :
        fs = cgi.FieldStorage(fp=env['wsgi.input'],environ=env)
        for i in fs.list :
            params[i.name] = fs.getfirst(i.name)
    start_response('200 OK',[('Content-type','text/html'),])
    response = wsgi_response(params)
    return response

if __name__ == '__main__' :
    
    if 2 == len(sys.argv) :
        port = int(sys.argv[1])
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',stream=sys.stdout)
        httpd = wsgiref.simple_server.make_server('',port,wsgi)
        logging.info('serving on %d ...' % port)
        httpd.serve_forever()

    else :
        
        def start_response(status,headers) :
            for i in headers :
                print '%s: %s' % (i[0],i[1])
            print
        
        env = {}
        env['REQUEST_METHOD'] = 'POST'
        env['wsgi.input'] = sys.stdin
        content = wsgi(env,start_response)
        print ''.join(content)

