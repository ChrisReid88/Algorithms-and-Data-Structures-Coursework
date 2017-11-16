'''
Simple draughts console game created by Chris Reid 05/10/17
Matric = 40202859
Module code = Set091117
Module title = Algorithms and data structures.
'''

# Random for AI choices, copy to create a deep copy of the stack and deque for
# the redo feature.
import random
import copy
from collections import deque
import crayons

# Global variables for the amount of players, a stack for undo and deque for redo,
# a list that stores all the moves in a game to be stored in a file and fed back.
humans = 0
undo_stack = []
redo_stack = deque()
game_history = []
history_row = 0


# Board for testing
board = [['-','-','-','-','-','-','-','-'],
         ['w','-','-','-','-','-','-','-'],
         ['-','b','-','-','b','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['-','b','-','b','-','b','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['-','w','-','-','-','-','B','-'],
         ['-','-','-','-','-','-','-','-']]

# # The actual board
# board = [['-','w','-','w','-','w','-','w'],
#          ['w','-','w','-','w','-','w','-'],
#          ['-','w','-','w','-','w','-','w'],
#          ['-','-','-','-','-','-','-','-'],
#          ['-','-','-','-','-','-','-','-'],
#          ['b','-','b','-','b','-','b','-'],
#          ['-','b','-','b','-','b','-','b'],
#          ['b','-','b','-','b','-','b','-']]

# Top of the board to be displayed
top = '  0   1   2   3   4   5   6   7'


# Updates and displays the current state of the board
def update_state():
    print(top)
    i = 0
    for row in board:
        print i, ' | '.join(map(str, row))
        i = i + 1
        print '  -----------------------------'


# Start game function that requests the amount of players
def start_game():

    global humans
    global undo_stack
    global redo_stack

    # Input and validation ensuring that only 0, 1 or 2 can be entered.
    number = raw_input("Please enter how many people are playing (0, 1 or 2) : ")
    try:
        humans = int(number)
    except ValueError:
        print "%s is not correct. Please enter '0, 1 or 2' for players" % number
        start_game()
    else:
        if humans >=0 and humans <= 2:
            # Add the initial state of the board to the undo stack and redo deque
            temp = copy.deepcopy(board)
            undo_stack.append(temp)
            white_move()
        else:
            # If the conditions are not met, alert the user and re-execute this function
            print "%d is not correct. Please enter '0, 1 or 2' for players" % humans
            start_game()


# Selecting and moving the white piece
def white_move():

    # Global variables so that they can be changed within the function
    global board
    global undo_stack
    global game_history
    global redo_stack
    global history_row

    # Display the current state of the board at the beginning of the turn
    update_state()

    # Variables with details of white team and displays what teams go it is
    white_pieces = ['w', 'W']
    player = 'w'
    print 'WHITES TURN'

    # If the player is AI (White is AI if only one person is playing)
    if humans < 2:
        # If there are white pieces with moves, select a random piece from the list
        # and tell the user what choice was made
        if len(pieces_with_moves(board, 'w')) > 0:
            piece_to_move = random.choice(pieces_with_moves(board, 'w'))
            row_number = int(piece_to_move[1])
            col_number = int(piece_to_move[0])
            print "AI chooses the piece at", col_number, row_number
        # If there are no available moves, its a draw and exit the game
        else:
            print "No more available moves. Draw! "
            exit()
    # Code for replaying a game from the text file. Calls in the row and removes the new line escape character.
    # When a row is read, it  goes to the next.
    elif humans == 3:
        piece_to_move = replay()[history_row].strip('\n')
        history_row = history_row + 1
        row_number = int(piece_to_move[1])
        col_number = int(piece_to_move[0])
        print "Player chooses the piece at", col_number, row_number
    # If the player is not AI but there are no available moves, its a draw and exit
    else:
        if len(pieces_with_moves(board, 'w')) == 0:
            print "No more moves available. Draw!"
            exit()
        # If white pieces have moves available to them, display those pieces coords. User then enters
        # the coords of the piece they wish to move.
        else:
            print "Pieces that have moves available: ", pieces_with_moves(board, 'w')
            piece_to_move = raw_input('Select the piece you wish to move ("u" to undo or "r" for redo): ')
            # Validation for input
            try:
                int(piece_to_move)
            except ValueError:
                try:
                    piece_to_move == 'r'
                except ValueError:
                    try:
                        piece_to_move == 'u'
                    except ValueError:
                        print "%s is not correct. Please enter a row number and col number (eg 27)" % piece_to_move
                        white_move()

            # If player enters 'u' and there is only the starting board in the stack, alert them and
            # restart their move
            if piece_to_move == 'u':
                if len(undo_stack) == 1:
                    print "Nothing left to undo."
                    white_move()
                # If there are other states in the stack, remove from the stack and append to deque, then
                # set the board to the last state within the stack.
                else:
                    redo_stack.append(undo_stack.pop())
                    board = undo_stack[-1]
                    black_move()
            # If player enters 'r' for redo and there is only starting board in the deque, alert them and restart their
            # move.
            elif piece_to_move == 'r':
                if len(redo_stack) == 1:
                    print "Nothing left to redo"
                    black_move()
                # If there are states in the deque, pop from the left of the deck and append it to the stack
                # before setting the board to the previous state in the deque
                else:
                    if redo_stack:
                        board = redo_stack[-1]
                        undo_stack.append(redo_stack.pop())
                        black_move()
                    else:
                        print "Nothing more to redo!"
                        white_move()
            # If the user entered coords, assign them to the variables
            else:
                row_number = int(piece_to_move[1])
                col_number = int(piece_to_move[0])

    # Append the piece that was selected to the game history list.
    game_history.append(piece_to_move)

    # If wrong colour is selected, alert user and restart whites turn
    if board[row_number][col_number] == 'b':
        update_state()
        print 'Wrong piece. You are whites.'
        white_move()

    # If empty space is picked, alert user and restart whites turn.
    if board[row_number][col_number] == '-':
        update_state()
        print 'You selected an empty square! Try again.'
        white_move()

    # If the selected square is a white piece
    if board[row_number][col_number] in white_pieces:

        # If the selected piece is a king add the blacks movements to the available move list
        if board[row_number][col_number] == 'W':
            king_moves = available_moves_up(row_number, col_number, 'white_king')
            moves = available_moves_down(row_number, col_number, 'w')
            moves = king_moves + moves
            for ele in moves:
                if row_number - int(ele[1]) == 2 or row_number - int(ele[1]) == -2:
                    moves = []
                    moves.append("%d%d" % (int(ele[0]), int(ele[1])))
                    print moves
        else:
            moves = available_moves_down(row_number, col_number, 'w')


        # If there are moves available display them. If not, alert user no moves available
        # and restart their move
        if moves:
            print 'Moves available: ', moves
        else:
            print 'No moves are available'
            white_move()

        # If player is AI select a random move from the available moves list of the previously selected
        # piece. Enter to continue to make it easier to follow
        if humans < 2:
            place_to_move = random.choice(moves)
            print 'AI chooses to move to ', place_to_move
            raw_input("Press enter to continue")
        elif humans == 3:
            place_to_move = replay()[history_row].strip('\n')
            history_row = history_row + 1
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])
            print "Player moves to ", col_number2, row_number2
            raw_input("Press enter to continue")
        else:
            # Get the position they wish to move their piece too
            place_to_move = raw_input('Where do you wish to move to?: ')

        # If that place is in the available moves list..
        if place_to_move in moves:
            # Coords of new position
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])
            game_history.append(place_to_move)

            # Enter the piece into the the new square. Either normal or kinged
            # and make the original square empty
            if board[row_number][col_number] == 'w':
                board[row_number2][col_number2] = 'w'
            else:
                board[row_number2][col_number2] = 'W'
            board[row_number][col_number] = '-'

            # If the position changed was a 2 square jump, replace the middle one with a
            # an empty square (Taking a piece).(added opposite for king pieces.)
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

            double_jump(board, row_number2, col_number2)

            # Check after every move if the enemy has piece on the board. If not
            # declare whites the winner. If so, append the board state to the stack and change to blacks move.
            ww = white_win(board)
            if ww:
                print 'WHITE WINS!'
                quit()
            elif double_jump(board, row_number2, col_number2, ):
                white_move()
            else:
                temp = copy.deepcopy(board)
                undo_stack.append(temp)
                black_move()

        # If the selected square is not in  the available list, alert user and restart
        # their turn.
        else:
            update_state()
            print 'Sorry, move not available!'
            white_move()


# Selecting and moving the white piece
def black_move():

    global board
    global undo_stack
    global game_history
    global history_row

    # Display the current state of the board at the beginning of the turn
    update_state()

    # Variables with details of white team and displays what teams go it is
    player = 'b'
    black_pieces = ['b', 'B']
    print'BLACKS TURN'

    # If there are no humans playing (for 1 human, white will always be the AI)
    if humans == 0:
        # If there are black pieces with moves, select a random piece from the list
        # and tell the user what choice was made
        if len(pieces_with_moves(board, 'b')) > 0:
            piece_to_move = random.choice(pieces_with_moves(board, 'b'))
            row_number = int(piece_to_move[1])
            col_number = int(piece_to_move[0])
            print "AI chooses the piece at", col_number, row_number
        # If there are no available moves, its a draw and exit the game
        else:
            print "No more available moves. It's a draw!"
            exit()
    elif humans == 3:
        piece_to_move = replay()[history_row].strip('\n')
        history_row = history_row + 1
        row_number = int(piece_to_move[1])
        col_number = int(piece_to_move[0])
        print "Player chooses the piece at", col_number, row_number
        raw_input('')
    # If the player is not AI but there are no available moves, its a draw and exit
    else:
        if len(pieces_with_moves(board, 'w')) == 0:
            print "No more moves available. Draw!"
            exit()
        # If black pieces have moves available to them, display those pieces coords. User then enters
        # the coords of the piece they wish to move.
        else:
            print "Pieces that have moves available: ", pieces_with_moves(board, 'b')
            piece_to_move = raw_input('Select the piece you wish to move: ')

            # Validation on input.
            try:
                int(piece_to_move)
            except ValueError:
                try:
                    piece_to_move == 'u'
                except ValueError:
                    try:
                        piece_to_move == 'r'
                    except ValueError:
                        print "%s is not correct. Please enter a row number and col number (eg 27)" % piece_to_move
                        black_move()

            # If player enters 'u' and there is only the starting board in the stack, alert them and
            # restart their move
            if piece_to_move == 'u':
                if len(undo_stack) == 1:
                    print "Nothing left to undo"
                    black_move()
                # If there are other states in the stack, remove from the stack and append to deque, then
                # set the board to the last state within the stack.
                else:
                    redo_stack.append(undo_stack.pop())
                    board = undo_stack[-1]
                    white_move()
                # If player enters 'r' for redo and there is only starting board in the deque, alert them and restart their
                # move.
            elif piece_to_move == 'r':
                if redo_stack:
                    board = redo_stack[-1]
                    undo_stack.append(redo_stack.pop())
                    white_move()
                else:
                    print "Nothing more to redo!"
                    black_move()
            # If the user entered coords, assign them to the variables
            else:
                row_number = int(piece_to_move[1])
                col_number = int(piece_to_move[0])

    # Store the piece selected in the game history list
    game_history.append(piece_to_move)

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

    # If the selected square is a black piece
    if board[row_number][col_number] in black_pieces:

        # If the selected piece is a king add the blacks movements to the available move list
        if board[row_number][col_number] == 'B':
            king_moves = available_moves_down(row_number, col_number, 'black_king')
            moves = available_moves_up(row_number, col_number, 'b')
            moves = king_moves + moves
            for ele in moves:
                if row_number - int(ele[1]) == 2 or row_number - int(ele[1]) == -2:
                    moves = []
                    moves.append("%d%d" % (int(ele[0]), int(ele[1])))
                    print moves
        else:
            moves = available_moves_up(row_number, col_number, 'b')

        # If the moves list is not empty, display the available moves, else display no moves available
        # and restart their turn
        if moves:
            print 'Moves available: ', moves
        else:
            print 'No moves are available'
            black_move()

        # If player is AI select a random move from the available moves list of the previously selected
        # piece. Enter to continue to make it easier to follow
        if humans == 0:
            place_to_move = random.choice(moves)
            print 'AI chooses to move to ', place_to_move
            raw_input("Press enter to continue")
        elif humans == 3:
            place_to_move = replay()[history_row].strip('\n')
            history_row = history_row + 1
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])
            print "Player moves to ", col_number2, row_number2
            raw_input("Press enter to continue")
        else:
            # Get the position they wish to move their piece to
            place_to_move = raw_input('Where do you wish to move to?: ')

        # If that place is in the available moves list..
        if place_to_move in moves:
            # Coords of new position
            row_number2 = int(place_to_move[1])
            col_number2 = int(place_to_move[0])

            # Append the coords of where the piece is being moved to to the history list.
            game_history.append(place_to_move)

            # Enter the piece into the the new square. Either normal or kinged
            # and make the original square empty
            if board[row_number][col_number] == 'b':
                board[row_number2][col_number2] = 'b'
            else:
                board[row_number2][col_number2] = 'B'
            board[row_number][col_number] = '-'

            # If the position changed was a 2 square jump, replace the middle one with a
            # an empty square (Taking a piece).(added opposite for king pieces.)
            if col_number2 - col_number == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number+1] = '-'
            elif col_number - col_number2 == 2 and row_number - row_number2 == 2:
                board[row_number-1][col_number-1] = '-'
            if col_number2 - col_number == 2 and row_number2 - row_number == 2:
                board[row_number + 1][col_number + 1] = '-'
            elif col_number - col_number2 == 2 and row_number2 - row_number == 2:
                board[row_number + 1][col_number - 1] = '-'

            # Check if piece has reached the opponents side of board. If so
            # change to a king( b -> B )
            kinging(row_number2, col_number2, player)

            # Check after every move if the enemy has piece on the board. If not
            # declare black the winner. If so, append the board state to the stack and change to blacks move
            bw = black_win(board)
            if bw:
                print 'BLACK WINS!'
                quit()
            elif double_jump(board, row_number2, col_number2, ):
                white_move()
            else:
                temp = copy.deepcopy(board)
                undo_stack.append(temp)
                white_move()
        # If the selected square is not in  the available list, alert user and restart
        # their turn.
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
        if col < 6 and row != 6 and board[row+1][col+1] in opponent and board[row+2][col+2] == '-':
            move = str(col+2) + str(row+2)
            moves.append(move)
        elif col > 2 and row != 6 and board[row+1][col-1] in opponent and board[row+2][col-2] == '-':
            move = str(col-2) + str(row+2)
            moves.append(move)
        else:
            if row != 7 and col != 0 and board[row + 1][col - 1] == '-':
                move = str(col - 1) + str(row + 1)
                moves.append(move)
            if col != 7 and board[row + 1][col + 1] == '-':
                move = str(col + 1) + str(row + 1)
                moves.append(move)

    return moves


# Find out and display available moves for black pieces or kinged white pieces.
def available_moves_up(row, col, player):

    # Empty list to store valid moves
    moves = []

    # Creating a list containing the two opponents pieces
    if player == 'b':
        opponent = ['w', 'W']
    elif player == 'white_king':
        opponent = ['b', 'B']

    # Conditions for valid moves. Valid moves get appended to the list which then get returned.
    # Prevents pieces moving off the board.
    if row != 0:
        # Stores the jumping moves available in the moves list
        if col > 1 and row != 1 and board[row-1][col-1] in opponent and board[row-2][col-2] == '-':
            move = str(col-2) + str(row-2)
            moves.append(move)
        elif col < 6 and row != 1 and board[row-1][col+1] in opponent and board[row-2][col+2] == '-':
            move = str(col+2) + str(row-2)
            moves.append(move)
        else:
            # Stores normal moves available in the moves list
            if row != 0 and col != 7 and board[row - 1][col + 1] == '-':
                    move = str(col + 1) + str(row - 1)
                    moves.append(move)
            if row != 0 and col != 0 and board[row - 1][col - 1] == '-':
                    move = str(col - 1) + str(row - 1)
                    moves.append(move)
    return moves


# Check if there are any black pieces left on the board, and if not
# return that the white team has won
def white_win(game_board):

    if not any('b' in sublist for sublist in game_board) and not any('B' in sublist for sublist in game_board):
        store_history(game_history)
        return True


# Check if there are any white pieces left on the board, and if not
# return that the black team has won
def black_win(game_board):

    if not any('w' in sublist for sublist in game_board) and not any('W' in sublist for sublist in game_board):
        # print "Game over! Whites Win!"
        store_history(game_history)
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
            if available_moves_up(t[1], t[0], 'white_king'):
                if int(available_moves_up(t[1], t[0], 'white_king')[0][1]) - t[1] == 2 or int(available_moves_up(t[1], t[0], 'white_king')[0][1]) - t[1] == -2:
                    available_takes.append("%d%d" % (t[0], t[1]))
                if "%d%d" % (t[0], t[1]) not in available_moves:
                    available_moves.append("%d%d" % (t[0], t[1]))
                else:
                    available_moves.append("%d%d" % (t[0], t[1]))
        elif piece == 'b':
            if available_moves_up(t[1], t[0], 'b'):
                if int(available_moves_up(t[1], t[0], 'b')[0][1]) - t[1] == -2:
                    available_takes.append("%d%d" % (t[0], t[1]))
                elif not available_takes:
                    available_moves.append("%d%d" % (t[0], t[1]))
            if available_moves_down(t[1], t[0], 'black_king'):
                if int(available_moves_down(t[1], t[0], 'black_king')[0][1]) - t[1] == 2 or int(
                        available_moves_down(t[1], t[0], 'black_king')[0][1]) - t[1] == -2:
                    available_takes.append("%d%d" % (t[0], t[1]))
                if "%d%d" % (t[0], t[1]) not in available_moves:
                    available_moves.append("%d%d" % (t[0], t[1]))
                else:
                    available_moves.append("%d%d" % (t[0], t[1]))
    # If there are any takes available, display them to use, else,
    # display other available moves.
    if available_takes:
        takes_set = list(set(available_takes))
        return takes_set
    else:
        takes_set = list(set(available_moves))
        return takes_set


# Stores the history list into a text file called "history.txt"
def store_history(hist):
    f = open('history.txt', 'w')
    for ele in hist:
        f.write(ele + '\n')
    f.close()


# Pulls the entries from the history text file and returns it as a list.
def replay():
    with open('history.txt', 'r') as f:
        game = f.readlines()
    return game


# Decide if the user wants to play or watch. If watch, set humans to '3'
# If play start the game normally.
def play_or_watch():
    global humans
    option = raw_input("Enter 'p' to play or 'w' to watch previous game: ")
    if option != 'p' and option != 'w':
        print "Sorry, wrong input."
        play_or_watch()
    else:
        if option == 'p':
            start_game()
        if option == 'w':
            humans = 3
            white_move()


def double_jump(gameboard, row, col):
    piece = gameboard[row][col]
    print piece

    if piece == 'w':
        moves = available_moves_down(row,col,'w')
        for ele in moves:
            if row - int(ele[1]) == -2:
                return True
    elif piece == 'b':
        moves = available_moves_down(row, col, 'w')
        for ele in moves:
            if row - int(ele[1]) == 2:
                return True
    elif piece == 'B' or piece == 'W':
        moves = available_moves_up(row, col, 'white_king')
        moves2 = available_moves_down(row, col, 'black_king')
        moves = moves + moves2
        for ele in moves:
            if row - int(ele[1]) == -2 or row - int(ele[1]) == 2:
                return True


# Initiate the game.
play_or_watch()