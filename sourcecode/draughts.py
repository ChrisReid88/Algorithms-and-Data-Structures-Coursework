'''
Simple draughts console game created by Chris Reid 05/10/17
Matric = 40202859
Module code = Set091117
Module title = Algorithms and data structures.
'''


# Board for testing
board = [['-','-','-','b','-','b','-','-'],
         ['-','-','-','-','W','-','-','-'],
         ['-','-','-','b','-','b','-','-'],
         ['-','-','w','-','-','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['-','b','-','-','-','-','-','-'],
         ['-','-','-','-','-','B','w','-'],
         ['-','-','-','-','w','-','-','-']]

# The actual board
# board = [['-','w','-','w','-','w','-','w'],
#          ['w','-','w','-','w','-','w','-'],
#          ['-','w','-','w','-','w','-','w'],
#          ['-','-','-','-','-','-','-','-'],
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

    update_state()
    # Variables with details of white team
    white_pieces = ['w', 'W']
    player = 'w'

    print 'WHITES TURN'
    pieces_with_moves(board, 'w')

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
        moves = available_moves_down(row_number, col_number, player)

        # If the selected piece is a king add the blacks movements to the available move list
        if board[row_number][col_number] == 'W':
            king_moves = available_moves_up(row_number, col_number, 'white_king')
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
            update_state()
            print 'Sorry, move not available!'
            white_move()


# Selecting and moving the white piece
def black_move():
    update_state()

    player = 'b'
    black_pieces = ['b', 'B']
    pieces_with_moves(board, 'b')
    print'BLACKS TURN'
    piece_to_move = raw_input('Select the piece you wish to move: ')
    row_number = int(piece_to_move[1])
    col_number = int(piece_to_move[0])

    # If wrong colour is selected, alert user and restart whites turn
    if board[row_number][col_number] == 'w':
        update_state()
        print 'Wrong piece, genius. You are blacks.'
        # black_move()

    # If empty space is picked, alert user and restart whites turn.
    if board[row_number][col_number] == '-':
        update_state()
        print 'You selected an empty square! Try again.'
        # black_move()

    if board[row_number][col_number] in black_pieces:

        moves = available_moves_up(row_number, col_number, 'b')

        # If the selected piece is a king add the blacks movements to the available move list
        if board[row_number][col_number] == 'B':
            king_moves = available_moves_down(row_number, col_number, 'black_king')
            moves = moves + king_moves

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
            if col_number2 - col_number == 2 and row_number2 - row_number == 2:
                board[row_number + 1][col_number + 1] = '-'
            elif col_number - col_number2 == 2 and row_number2 - row_number == 2:
                board[row_number + 1][col_number - 1] = '-'

            print row_number2
            print col_number2
            kinging(row_number2, col_number2, player)

            bw = black_win(board)

            if bw:
                print 'BLACK WINS!'
            else:
                white_move()
        else:
            print 'Sorry, move not available!'
            black_move()


# Find out and display available moves for white pieces or kinged black pieces
def available_moves_down(row, col, player):

    # Empty list to store valid moves
    moves = []

    # Creating a list containing the two opponents pieces
    if player == 'w':
        opponent = ['b', 'B']
    elif player == 'black_king':
        opponent = ['w', 'W']

    # Conditions for valid moves. Valid moves get appended to the list which then get returned.
    # Prevents pieces moving off the board.
    if row != 7:
        if col != 7 and row < 6 and board[row+1][col+1] in opponent and board[row+2][col+2] == '-':
            move = str(col+2) + str(row+2)
            moves.append(move)
        elif col != 0 and row < 6 and board[row+1][col-1] in opponent and board[row+2][col-2] == '-':
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


# Find out and display available moves for black pieces or kinged white pieces.
def available_moves_up(row, col, player):

    #Empty list to store valid moves
    moves = []

    # Creating a list containing the two opponents pieces
    if player == 'b':
        opponent = ['w', 'W']
    elif player == 'white_king':
        opponent = ['b', 'B']

    # Conditions for valid moves. Valid moves get appended to the list which then get returned.
    # Prevents pieces moving off the board.
    if row != 7:
        if col != 0 and row > 1 and board[row-1][col-1] in opponent and board[row-2][col-2] == '-':
            move = str(col-2) + str(row-2)
            moves.append(move)
        elif col != 7 and row > 1 and board[row-1][col+1] in opponent and board[row-2][col+2] == '-':
            move = str(col+2) + str(row-2)
            moves.append(move)
        else:
            if col != 0 and board[row - 1][col + 1] == '-':
                move = str(col + 1) + str(row - 1)
                moves.append(move)
            if col != 7 and board[row - 1][col - 1] == '-':
                move = str(col - 1) + str(row - 1)
                moves.append(move)

    return moves


# Check if there are any black pieces left on the board, and if not
# return that the white team has won
def white_win(game_board):

    if not any('b' in sublist for sublist in game_board):
        # print "Game over! Whites Win!"
        return True


# Check if there are any white pieces left on the board, and if not
# return that the black team has won
def black_win(game_board):

    if not any('w' in sublist for sublist in game_board):
        # print "Game over! Whites Win!"
        return True


# King a piece when it reaches the opponents side of the board
def kinging(row, col, player):

    if row == 7 and player == 'w':
        board[row][col] = 'W'
    if row == 0 and player == 'b':
        board[row][col] = 'B'


# Find out which pieces have available moves and display them to the user.
# To be used for the AI opponent
def pieces_with_moves(game_board, piece):

    # Empty lists to store the pieces, moves and if any, available takes.
    available_pieces = []
    available_moves = []
    available_takes = []

    # Declaring the kings of the pieces when they are passed to the function
    if piece == 'w':
        king = 'W'
    elif piece == 'b':
        king = 'B'

    # Traverses the board and returns only the pieces that have available moves.
    if piece:
        available_pieces = [(iy, ix) for ix, row in enumerate(game_board) for iy, i in enumerate(row) if i == piece or i == king]

    # Check that any of the pieces in the available_piece list can take an opponents piece. If true, add
    # them to the available_takes list. If not, add all other moves to the available_moves list.
    for t in available_pieces:
        if piece == 'w':
            if available_moves_down(t[1], t[0], 'w'):
                if int(available_moves_down(t[1], t[0], 'w')[0][1]) - t[1] == 2:
                    available_takes.append("%d%d" % (t[0], t[1]))
                elif not available_takes:
                    available_moves.append("%d%d" % (t[0], t[1]))
        elif piece == 'b':
            if available_moves_up(t[1], t[0], 'b'):
                if int(available_moves_up(t[1], t[0], 'w')[0][1]) + t[1] == 2:
                    available_takes.append("%d%d" % (t[0], t[1]))

                elif not available_takes:
                    available_moves.append("%d%d" % (t[0], t[1]))

    # If there are any takes available, display them to use, else,
    # display other available moves.
    if available_takes:
        print "Pieces with moves available: ", available_takes
    else:
        print "Pieces with moves available: ", available_moves

# Initiate the game.
white_move()

# for i, x in enumerate(game_board):
#     if king in x:
#         available_pieces.append("%d%d" % (x.index(king), i))
#
# for i, x in enumerate(game_board):
#     if piece in x:
#         available_pieces.append("%d%d" % (x.index(piece), i))


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

