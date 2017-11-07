board = [['-','-','-','-','-','-','-','-'],
         ['-','-','-','-','w','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['-','-','b','-','-','-','b','-'],
         ['-','-','-','W','-','-','-','-'],
         ['-','-','-','-','b','-','-','-'],
         ['-','w','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-','-']]


# board = [['-','w','-','w','-','w','-','w'],
#          ['w','-','w','-','w','-','w','-'],
#          ['-','w','-','w','-','w','-','w'],
#          ['-','-','-','-','b','-','-','-'],
#          ['-','-','-','-','-','-','-','-'],
#          ['b','-','b','-','b','-','b','-'],
#          ['-','b','-','b','-','b','-','b'],
#          ['b','-','b','-','b','-','b','-']]


top = '  0   1   2   3   4   5   6   7'


def update_state():
    print(top)   
    i = 0
    for row in board:
        print i, ' | '.join(map(str, row))
        i = i + 1
        print '  -----------------------------'


# Selecting and moving the white piece
def white_move():
    # Variables with details of white team
    white_pieces = ['w', 'W']
    player = 'white'

    update_state()
    print 'WHITES TURN'

    # The piece the white team wishes to select. (Across then down)
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

    # If the selected square is a white piece
    if board[row_number][col_number] in white_pieces:

        # Retrieve the available moves
        moves = available_white_moves(row_number, col_number, player)

        # If the selected piece is a king add the blacks movements to the available move list
        if board[row_number][col_number] == 'W':
            king_moves = available_black_moves(row_number, col_number, 'white_king')
        moves = moves + king_moves

        # If there are moves available display them. If not, alert user no moves available
        # and restart their move
        if moves:
            print 'Moves available: ', moves
        else:
            print 'No moves are available'
            white_move()

        # Get the position they wish to move their piece too
        place_to_move = raw_input('Where do you wish to move to?: ')

        # If that place is in the available moves list..
        if place_to_move in moves:
            # Coords of new position
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])

            # Enter the piece into the the new square. Either normal or kinged
            # and make the original square empty
            if board[row_number][col_number] == 'w':
                board[row_number2][col_number2] = 'w'
            else:
                board[row_number2][col_number2] = 'W'
            board[row_number][col_number] = '-'

            # If the position changed was a 2 square jump, replace the middle one with a
            # an empty square (Taking a piece).(added opposite for king pieces.)5
            if col_number2 - col_number == 2 and row_number2 - row_number == 2:
                board[row_number+1][col_number+1] = '-'
            elif col_number - col_number2 == 2 and row_number2 - row_number == 2:
                board[row_number+1][col_number-1] = '-'
            if col_number2 - col_number == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number+1] = '-'
            elif col_number - col_number2 == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number-1] = '-'

            # Check if piece has reached the opponents side of board. If so
            # change to a king( w -> W )
            kinging(row_number2, col_number2, player)

            # Check after every move if the enemy has piece on the board. If not
            # declare whites the winner. If so, change to blacks move.
            ww = white_win(board)
            if ww:
                print 'WHITE WINS!'
            else:
                black_move()

        # If the selected square is not in  the available list, alert user and restart
        # their turn.
        else:
            print 'Sorry, move not available!'
            white_move()


# Selecting and moving the white piece
def black_move():
    black_pieces = ['b', 'B']
    update_state()
    print'BLACKS TURN'
    piece_to_move = raw_input('Select the piece you wish to move: ')
    row_number = int(piece_to_move[1])
    col_number = int(piece_to_move[0])

    # If wrong colour is selected, alert user and restart whites turn
    if board[row_number][col_number] == 'w':
        update_state()
        print 'Wrong piece, genius. You are blacks.'
        black_move()

    # If empty space is picked, alert user and restart whites turn.
    if board[row_number][col_number] == '-':
        update_state()
        print 'You selected an empty square! Try again.'
        black_move()

    if board[row_number][col_number] in black_pieces:

        moves = available_black_moves(row_number, col_number, 'black')

        if moves:
            print 'Moves available: ', moves
        else:
            print 'No moves are available'
            black_move()

        place_to_move = raw_input('Where do you wish to move to?: ')
        if place_to_move in moves:

            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])

            if board[row_number][col_number] == 'b':
                board[row_number2][col_number2] = 'b'
            else:
                board[row_number2][col_number2] = 'B'

            board[row_number][col_number] = '-'

            if col_number2 - col_number == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number+1] = '-'
            elif col_number - col_number2 == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number-1] = '-'

            bw = black_win(board)

            if bw:
                print 'BLACK WINS!'
            else:
                white_move()
        else:
            print 'Sorry, move not available!'
            black_move()


# Find out and display available moves
def available_white_moves(row, col, player):
    if player == 'white':
        opponent = ['b', 'B']
    elif player == 'black_king':
        opponent = ['w', 'W']

    moves = []

    if col != 7 and board[row+1][col+1] in opponent and board[row+2][col+2] == '-':
        move = str(col+2) + str(row+2)
        moves.append(move)
    elif col != 0 and board[row+1][col-1] in opponent and board[row+2][col-2] == '-':
        move = str(col-2) + str(row+2)
        moves.append(move)
    else:
        if col != 0 and board[row + 1][col - 1] == '-':
            move = str(col - 1) + str(row + 1)
            moves.append(move)
        if col != 7 and board[row + 1][col + 1] == '-':
            move = str(col + 1) + str(row + 1)
            moves.append(move)

    return moves


# Find out and display available moves
def available_black_moves(row, col, player):
    moves = []

    if player == 'black':
        opponent = ['w', 'W']
    elif player == 'white_king':
        opponent = ['b', 'B']

    if col != 7 and board[row-1][col-1] in opponent and board[row-2][col-2] == '-':
        move = str(col-2) + str(row-2)
        moves.append(move)
    elif col != 0 and board[row-1][col+1] in opponent and board[row-2][col+2] == '-':
        move = str(col+2) + str(row-2)
        moves.append(move)
    else:
        if col != 7 and board[row - 1][col + 1] == '-':
            move = str(col + 1) + str(row - 1)
            moves.append(move)
        if col != 0 and board[row - 1][col - 1] == '-':
            move = str(col - 1) + str(row - 1)
            moves.append(move)

    return moves


def white_win(game_board):
    if not any('b' in sublist for sublist in game_board):
        # print "Game over! Whites Win!"
        return True


def black_win(game_board):
    if not any('w' in sublist for sublist in game_board):
        # print "Game over! Whites Win!"
        return True


def kinging(row, col, player):
    if row == 7 and player == 'white':
        board[row][col] = 'W'
    elif row == 0 and player == 'black':
        board[row][col] == 'B'

white_move()


# Find out and display available moves
# def available_moves(row, col, player):
#     moves = []
#
#     if player == 'white':
#         piece = 'b'
#         if col != 0 and board[row + 1][col - 1] == '-':
#             move = str(col - 1) + str(row + 1)
#             moves.append(move)
#         if col != 7 and board[row + 1][col + 1] == '-':
#             move = str(col + 1) + str(row + 1)
#             moves.append(move)
#         if col != 7 and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == '-':
#             move = str(col + 2) + str(row + 2)
#             moves.append(move)
#         if col != 0 and board[row + 1][col - 1] == piece and board[row + 2][col - 2] == '-':
#             move = str(col - 2) + str(row + 2)
#             moves.append(move)
#     elif player == 'black':
#         piece = 'w'
#         if col != 7 and board[row - 1][col + 1] == '-':
#             move = str(col + 1) + str(row - 1)
#             moves.append(move)
#         if col != 0 and board[row-1][col-1] == '-':
#             move = str(col-1) + str(row-1)
#             moves.append(move)
#         if col != 7 and board[row-1][col-1] == piece and board[row-2][col-2] == '-':
#             move = str(col-2) + str(row-2)
#             moves.append(move)
#         if col != 0 and board[row-1][col+1] == piece and board[row-2][col+2] == '-':
#             move = str(col+2) + str(row-2)
#             moves.append(move)
#
#     return moves


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

