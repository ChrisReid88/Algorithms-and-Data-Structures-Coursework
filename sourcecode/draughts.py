board = [['-','w','-','w','-','w','-','w'],
         ['w','-','w','-','w','-','w','-'],
         ['-','w','-','w','-','w','-','w'],
         ['-','-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['b','-','b','-','b','-','b','-'],
         ['-','b','-','b','-','b','-','b'],
         ['b','-','b','-','b','-','b','-']]


top = '  0   1   2   3   4   5   6   7'


def update_state():
    print(top)   
    i = 0
    for row in board:
        print i, ' | '.join(map(str, row))
        i = i + 1
        print '  -----------------------------'


update_state()


# Selecting and moving the white piece
def white_move():
    piece_to_move = raw_input('Select the piece you wish to move: ')
    row_number = int(piece_to_move[1])
    col_number = int(piece_to_move[0])

    # If wrong colour is selected, alert user and restart whites turn
    if board[row_number][col_number] == 'b':
        update_state()
        print 'Wrong piece, genius. You are whites.'
        white_move()

    # If empty space is picked, alert user and restart whites turn.
    if board[row_number][col_number] == '-':
        update_state()
        print 'You selected an empty square! Try again.'
        white_move()

    if board[row_number][col_number] == 'w':

        moves = available_moves(row_number, col_number)

        if moves:
            print 'Moves available: ', moves
        else:
            print 'No moves are available'
            white_move()

        place_to_move = raw_input('Where do you wish to move to?: ')
        if place_to_move in moves:
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])
            board[row_number2][col_number2] = 'w'
        else:
            print 'Sorry, move not available!'
            white_move()


# Find out and display available moves
def available_moves(row, col):
    # if col != 0 and col != 7:
    #     print 'Available moves are', row-1, col+1, 'and', row+1, col+1
    moves = []
    if col != 0 and board[row + 1][col - 1] == '-':
        move = str(col - 1) + str(row + 1)
        moves.append(move)
    if col != 7 and board[row+1][col+1] == '-':
        move = str(col+1) + str(row+1)
        moves.append(move)

    return moves


white_move()

update_state()

# def valid_white_move(row, col):
#     if board[row-1][col+1] == '-' and board[row+1][col+1]:
#         return True
#     return False


# def white_move():
#     peice_to_move = raw_input('Enter a peice to move(E.g 1 1): ')
#     x = int(peice_to_move[0])
#     y = int(peice_to_move[2])
#
#     if board[x][y] == 'w':
#         board[x][y] = '-'
#         place_to_move = raw_input('Select where you want to move: ')
#         x2 = int(place_to_move[0])
#         y2 = int(place_to_move[2])
#         if board[x][y] == '-':
#             board[x2][y2] = 'w'
#     else:
#         print "Sorry. Invalid selection"
#     update_state()

