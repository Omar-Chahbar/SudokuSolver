from array import *
from Solver import Solver
import copy
import sys

def solvePuzzle(boardString):
    boardArray = stringToArray(boardString)
    solver = Solver(boardArray)
    return solver.solvePuzzle()

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