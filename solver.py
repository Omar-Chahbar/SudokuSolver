from array import *

def solvePuzzle(boardString):
    boardArray = stringToArray(boardString)
    valid = checkInitialValidity(boardArray)
    if not valid:
        print("invalid board!")
        return
    return solvePuzzleRecursively(boardArray,0,0, "forward", boardArray)

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
    while not checkvalidity(board,row,column):
        board[row][column]+= 1
        if board[row][column] == 10:
            board[row][column] = 0
            return solvePuzzleRecursively(board,row,column - 1, "backwards", INITIAL_BOARD)

    return solvePuzzleRecursively(board,row,column + 1, "forward", INITIAL_BOARD)

def stringToArray(boardString):
    print("hi")
    row = boardString.split("/")
    board = [[]]
    
    for r in range (0,9):
        board.insert(r, row[r].split(','))
    board.pop(9)
    return board

def checkValidity(board, row, column):
    value = board[row][column]
    if board[row].count(value) > 1:
        return False
    if not validColumn(board,column,value):
        return False
    if not validBox(board,row,column,value):
        return False
    return True
    
def validColumn(board,column,value):
    columnList = []
    for row in baord:
        columnList.append(row[column])
    return columnList.count(value) == 1

def validBox(board,row,column,value):
    boxTopRow = 0
    boxTopColumn = 0

    if row >= 6:
        boxTopRow = 6
    elif row >= 3
        boxTopRow = 3

    if column >= 6:
        boxTopColumn = 6
    elif column >= 3
        boxTopColumn = 3

    box = []
    for  for r in range (boxTopRow,boxTopRow + 3):
        for c in range (boxTopColumn,boxTopColumn + 3):
            box.append(board[r][c])
    
    return box.count(value) == 1
    
def checkInitialValidity(board):
    if not InitialRowsValid(board)
        return False
    if not InitialColumnsValid(board)
        return False
    if not InitialBoxesValid(board)
        return False
    return True
    
def InitialRowsValid(board):
    for row in board:
        if hasDuplicates(row):
            return False
    return True  

def InitialColumnsValid(board):
    columnList = []
    for column in range (0,10)
        for row in board:
            columnList.append(row[column])
        if hasDuplicates(columnList):
            return False 
        columnList.clear()
    return True

def InitialBoxesValid(board):
    box = []
    for r in range(0,7,3):
        for c in range(0,7,3):
            box = buildBox(board,r,c)
            if hasDuplicates(box)
                return False
    return True
    
def buildBox(board,row,column):
    box = []

    for r in range(row, row + 3):
        for c in range(column, column + 3):
            box.append(board[r][c])
    return box

def hasDuplicates(list):
    difference = len(list) - len(set(list))
    if difference != row.count(0) - 1:
        return True
    return False

def init():

    BOARD_STRING = ""

    for x in range (1,10):
        for y in range (1,10):
            BOARD_STRING += str(y) + ","
        BOARD_STRING = BOARD_STRING[:-1]
        BOARD_STRING += "/"
    BOARD_STRING = BOARD_STRING[:-1]
    solvePuzzle(BOARD_STRING)

init()