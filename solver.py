from array import *

def solvePuzzle(boardString):
    boardArray = stringToArray(boardString)
    valid = checkInitialValidity(boardArray)
    if not valid:
        print("Invalid board!")
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
    while not checkValidity(board,row,column):
        board[row][column]+= 1
        if board[row][column] == 10:
            board[row][column] = 0
            return solvePuzzleRecursively(board,row,column - 1, "backwards", INITIAL_BOARD)

    return solvePuzzleRecursively(board,row,column + 1, "forward", INITIAL_BOARD)

def stringToArray(boardString):
    row = boardString.split("/")
    board = [[]]
    
    for r in range (0,9):
        board.insert(r, row[r].split(','))
    board.pop(9)

    for r in range (0,9):
        for c in range (0,9):
            board[r][c] = int(board[r][c])
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
    for row in board:
        columnList.append(row[column])
    return columnList.count(value) == 1

def validBox(board,row,column,value):
    boxTopRow = 0
    boxTopColumn = 0

    if row >= 6:
        boxTopRow = 6
    elif row >= 3:
        boxTopRow = 3

    if column >= 6:
        boxTopColumn = 6
    elif column >= 3:
        boxTopColumn = 3

    box = []
    for r in range (boxTopRow,boxTopRow + 3):
        for c in range (boxTopColumn,boxTopColumn + 3):
            box.append(board[r][c])
    
    return box.count(value) == 1
    
def checkInitialValidity(board):
    if not InitialRowsValid(board):
        return False
    if not InitialColumnsValid(board):
        return False
    if not InitialBoxesValid(board):
        return False
    return True
    
def InitialRowsValid(board):
    for row in board:
        if hasDuplicates(row):
            return False
    return True  

def InitialColumnsValid(board):
    columnList = []
    for column in range (0,9):
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
            if hasDuplicates(box):
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
    if difference != list.count(0) - 1:
        return True
    return False

def init():

    BOARD_STRING = ""

    # for x in range (1,10):
    #     for y in range (1,10):
    #         BOARD_STRING += str(y) + ","
    #     BOARD_STRING = BOARD_STRING[:-1]
    #     BOARD_STRING += "/"
    # BOARD_STRING = BOARD_STRING[:-1]
    row0 = "0,3,0,0,0,0,6,0,0/"  
    row1 = "5,0,2,0,0,9,7,0,0/" 
    row2 = "0,0,0,0,0,4,0,0,0/" 
    row3 = "7,1,0,0,2,0,0,0,3/" 
    row4 = "0,0,0,4,0,8,0,0,0/" 
    row5 = "6,0,0,0,9,0,0,5,7/" 
    row6 = "0,0,0,8,0,0,0,0,0/" 
    row7 = "0,0,4,3,0,0,5,0,9/" 
    row8 = "0,0,7,0,0,0,0,3,0"
    BOARD_STRING = row0 + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8
    solvedPuzzle = solvePuzzle(BOARD_STRING)
    # print (solvedPuzzle)

init()