board = [['-','w','-','w','-','w','-','w'],
         ['w','-','w','-','w','-','w','-'],
         ['-','w','-','w','-','w','-','w'],
         ['-','-','-','-','-','-','-','-'],
         ['-','-','-','-','-','-','-','-'],
         ['B','-','B','-','B','-','B','-'],
         ['-','B','-','B','-','B','-','B'],
         ['B','-','B','-','B','-','B','-']]

top = '  1   2   3   4   5   6   7   8'

def updateState():
    print(top)   
    i = 0
    for row in board:
        i = i + 1
        print(i,' | '.join(map(str,row)))
        print('  -----------------------------')
updateState()

def whiteMove():
    peiceToMove = input('Enter a peice to move(E.g 1 1): ')
    x = int(peiceToMove[0])
    y = int(peiceToMove[2])

    if board[x][y] == 'w':
        board[x][y] = '-'
        placeToMove = input('Select where you want to move: ')
        x2 = int(placeToMove[0])
        y2 = int(placeToMove[2])
        if board[x][y] == '-':
            board[x2][y2] = 'w'
    else:
        print("Sorry. Invalid selection")
    updateState()
    
whiteMove()
