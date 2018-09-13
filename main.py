from array import *
import copy
import sys

def solvePuzzle(boardString):
    boardArray = stringToArray(boardString)
    valid = checkInitialValidity(boardArray)
    if not valid:
        print("Invalid board!")
        return
    candidateTable = buildCandidateTable(boardArray)
    solveTrivialCells(boardArray,candidateTable)
    initialBoard = copy.deepcopy(boardArray)
    return solvePuzzleRecursively(boardArray,0,0, "forward", initialBoard,candidateTable)

def solvePuzzleRecursively(board, row, column, direction, initialBoard,candidateTable):
    if column > 8:
        if row >= 8:
            return board
        column = 0
        row+= 1
    
    if column < 0:
        column = 8
        row-= 1
        if row < 0:
            print("This board has no solution!")
            return

    if initialBoard[row][column] != 0:
        if direction == "forward":
            return solvePuzzleRecursively(board,row,column + 1, direction, initialBoard,candidateTable)
        else:
            return solvePuzzleRecursively(board,row,column - 1, direction, initialBoard,candidateTable)
 
    if board[row][column] == 9: 
        board[row][column] = 0
        return solvePuzzleRecursively(board,row,column - 1, "backwards", initialBoard,candidateTable)

    board[row][column]+= 1
    while not checkValidity(board,row,column):
        board[row][column]+= 1
        if board[row][column] == 10:
            board[row][column] = 0
            return solvePuzzleRecursively(board,row,column - 1, "backwards", initialBoard,candidateTable)

    return solvePuzzleRecursively(board,row,column + 1, "forward", initialBoard,candidateTable)

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
    boxTopRow = getBoxTopLeft(row)
    boxTopColumn = getBoxTopLeft(column)

    box = []
    for r in range (boxTopRow,boxTopRow + 3):
        for c in range (boxTopColumn,boxTopColumn + 3):
            box.append(board[r][c])
    
    return box.count(value) == 1

def getBoxTopLeft(index):
    if index >= 6:
        return 6
    elif index >= 3:
        return 3
    return 0

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
    if difference != list.count(0) - 1 and difference != 0:
        return True
    return False

def getCandidateValues(board,x,y):
    candidateValues = []

    for value in range(1,10):
        board[x][y] = value
        if checkValidity(board,x,y):
            candidateValues.append(value)
    board[x][y] = 0
    return candidateValues

def buildCandidateTable(board):
    candidateTable = [[0 for i in range(9)]for j in range(9)]

    for x in range(0,9):
        for y in range(0,9):
            if board[x][y] == 0:
                candidateTable[x][y] = getCandidateValues(board,x,y)

    return candidateTable

def updateCandidateTable(row,column,value, candidateTable):

    updateRow(candidateTable,row,value)
    updateColumn(candidateTable,column,value)   
    updateBox(candidateTable,row,column,value)

def updateRow(candidateTable,row,value):

    for x in candidateTable[row]:
        if x != 0 and x.count(value) == 1:
            x.remove(value)

def updateColumn(candidateTable,column,value):
    for row in candidateTable:
        if row[column] != 0 and row[column].count(value) == 1:
            row[column].remove(value)

def updateBox(candidateTable,row,column,value):
    topRow = getBoxTopLeft(row)
    topColumn = getBoxTopLeft(column)

    for x in range(topRow, topRow + 3):
        for y in range(topColumn, topColumn + 3):
            if candidateTable[x][y] != 0 and candidateTable[x][y].count(value) == 1:
                candidateTable[x][y].remove(value)

def solveTrivialCells(boardArray, candidateTable):

    changeMade = False
    solveTrivialSingleCells(boardArray, candidateTable, changeMade)
    solveHiddenCells(boardArray, candidateTable, changeMade)

    if changeMade = True:
        solveTrivialCells(boardArray, candidateTable)

def solveHiddenCells(boardArray, candidateTable,changeMade):
    checkHiddenRows(boardArray, candidateTable,changeMade)
    checkHiddenColumns(boardArray, candidateTable,changeMade)
    checkHiddenBoxes(boardArray, candidateTable,changeMade)

def checkHiddenRows(boardArray, candidateTable,changeMade):
    for i in range(0,9):
        missingValues = []
        for h in range(1,10):
            if boardArray[i].count(h) == 0:
                missingValues.append(h)
        
        for value in missingValues:
            countOfValue = 0
            index = 0
            for k in range(0,9):
                if candidateTable[i][k] != 0 and candidateTable[i][k].count(value) == 1:
                    countOfValue += 1
                    index = k
            if countOfValue == 1:
                boardArray[i][index] = candidateTable[i][index].pop()
                candidateTable[i][index] = []
                updateCandidateTable(i, index, boardArray[i][index], candidateTable)
                changeMade = True

def solveTrivialSingleCells(boardArray, candidateTable, changeMade):

    for x in range(0, 9):
        for y in range(0, 9):
            if boardArray[x][y] == 0 and len(candidateTable[x][y]) == 1:
                boardArray[x][y] = candidateTable[x][y].pop()
                candidateTable[x][y] = []
                updateCandidateTable(x, y, boardArray[x][y], candidateTable)
                changeMade = True

def getNextValueInList(list,value):
    index = list.index(value)

    if index == len(list) - 1:
        return -1
    return list[index + 1]

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
    sys.setrecursionlimit(2**20)
    solvedPuzzle = solvePuzzle(BOARD_STRING)
    print (solvedPuzzle)

init()