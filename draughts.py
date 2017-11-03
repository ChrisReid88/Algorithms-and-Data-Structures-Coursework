board = [['-','w','-','w','-','w','-','w'],
         ['w','-','w','-','w','-','w','-'],
         ['-','w','-','w','-','w','-','w'],
         ['-','-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['B','-','B','-','B','-','B','-'],
         ['-','B','-','B','-','B','-','B'],
         ['B','-','B','-','B','-','B','-']]

top = '  1   2   3   4   5   6   7   8'


def update_state():
    print(top)   
    i = 0
    for row in board:
        i = i + 1
        print i,' | '.join(map(str, row))
        print '  -----------------------------'


update_state()


def white_move():
    peice_to_move = raw_input('Enter a peice to move(E.g 1 1): ')
    x = int(peice_to_move[0])
    y = int(peice_to_move[2])

    if board[x][y] == 'w':
        board[x][y] = '-'
        place_to_move = raw_input('Select where you want to move: ')
        x2 = int(place_to_move[0])
        y2 = int(place_to_move[2])
        if board[x][y] == '-':
            board[x2][y2] = 'w'
    else:
        print "Sorry. Invalid selection"
    update_state()


white_move()
