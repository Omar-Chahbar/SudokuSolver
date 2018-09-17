from array import *
from Solver import Solver
from ValidationChecker import ValidationChecker
import sys

def solvePuzzle(boardString):
    boardArray = stringToArray(boardString)
    validationChecker = ValidationChecker()
    solver = Solver(boardArray,validationChecker)
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

    row0 = "0,0,0,9,0,0,0,6,3/"  
    row1 = "0,0,0,0,3,0,0,5,0/" 
    row2 = "0,0,0,0,0,0,1,8,0/" 
    row3 = "5,0,2,0,0,8,9,1,6/" 
    row4 = "1,0,0,4,0,6,8,2,7/" 
    row5 = "0,0,6,1,0,0,3,4,5/" 
    row6 = "0,1,7,0,0,0,0,0,0/" 
    row7 = "0,8,0,0,2,0,0,0,0/" 
    row8 = "6,2,0,0,0,4,0,0,0"
    BOARD_STRING = row0 + row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8
    sys.setrecursionlimit(2**20)
    solvedPuzzle = solvePuzzle(BOARD_STRING)
    print (solvedPuzzle)

init()