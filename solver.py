from array import *

def solvePuzzle(boardString, INITIAL_BOARD):
    boardArray = stringToArray(boardString, INITIAL_BOARD)
    valid = checkValidity(boardArray)
    if not valid:
        print("invalid board!")
        return
    return solvePuzzleRecursively(boardArray,0,0, "forward", INITIAL_BOARD)

def solvePuzzleRecursively(board, row, column, direction, INITIAL_BOARD):
    if column > 8:
        if row >= 8:
            return board
        column = 0
        row+= 1
    
    if column < 0:
        column = 9
        row-= 1
        if row < 0:
            print("This board has no solution!")
            return

    if INITIAL_BOARD[row][column] != 0:
        if direction == "forward":
            return solvePuzzleRecursively(board,row,column + 1, direction, INITIAL_BOARD)
        else:
            return solvePuzzleRecursively(board,row,column - 1, direction, INITIAL_BOARD)
 
    board[row][column]+= 1
    while not checkvalidity(board):
        board[row][column]+= 1
        if board[row][column] == 10:
            board[row][column] = 0
            return solvePuzzleRecursively(board,row,column - 1, "backwards", INITIAL_BOARD)

    return solvePuzzleRecursively(board,row,column + 1, "forward", INITIAL_BOARD)

def stringToArray(boardString, INITIAL_BOARD):
    print("hi")
    row = boardString.split("/")
    board = [[]]
    
    for r in range (0,9):
        board.insert(r, row[r].split(','))
    board.pop(9)
    INITIAL_BOARD = board
    print(INITIAL_BOARD)

def checkValidity(board):
    return True

def init():

    BOARD_STRING = ""
    INITIAL_BOARD = [[]]

    for x in range (1,10):
        for y in range (1,10):
            BOARD_STRING += str(y) + ","
        BOARD_STRING = BOARD_STRING[:-1]
        BOARD_STRING += "/"
    BOARD_STRING = BOARD_STRING[:-1]
    solvePuzzle(BOARD_STRING, INITIAL_BOARD)

init()