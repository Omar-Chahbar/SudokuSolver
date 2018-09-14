from ValidationChecker import ValidationChecker
from ValidationChecker import getBoxTopLeft

class Solver:
    boardArray: [[]]

    def __init__(self, boardArray):
        self.boardArray = boardArray

    def solvePuzzle(self):
        validationChecker = ValidationChecker()
        valid = validationChecker.checkInitialValidity(self.boardArray)
        if not valid:
            print("Invalid board!")
            return
        candidateTable = self.buildCandidateTable()
        self.solveTrivialCells(self.boardArray,candidateTable)
        initialBoard = copy.deepcopy(self.boardArray)
        self.solvePuzzleRecursively(0,0, "forward", initialBoard,candidateTable)

    def solvePuzzleRecursively(self, row, column, direction, initialBoard,candidateTable):
        if column > 8:
            if row >= 8:
                return self.boardArray
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
                return self.solvePuzzleRecursively(row,column + 1, direction, initialBoard,candidateTable)
            else:
                return self.solvePuzzleRecursively(row,column - 1, direction, initialBoard,candidateTable)
    
        if board[row][column] == 9: 
            board[row][column] = 0
            return self.solvePuzzleRecursively(row,column - 1, "backwards", initialBoard,candidateTable)

        board[row][column]+= 1
        while not checkValidity(row,column):
            board[row][column]+= 1
            if board[row][column] == 10:
                board[row][column] = 0
                return self.solvePuzzleRecursively(row,column - 1, "backwards", initialBoard,candidateTable)

        return self.solvePuzzleRecursively(row,column + 1, "forward", initialBoard,candidateTable)

    def buildCandidateTable(self):
        candidateTable = [[0 for i in range(9)]for j in range(9)]

        for x in range(0,9):
            for y in range(0,9):
                if self.boardArray[x][y] == 0:
                    candidateTable[x][y] = self.getCandidateValues(x,y)

        return candidateTable

    def getCandidateValues(self,x,y):
        candidateValues = []

        for value in range(1,10):
            self.boardArray[x][y] = value
            if checkValidity(board,x,y):
                candidateValues.append(value)
        self.boardArray[x][y] = 0
        return candidateValues

    def updateCandidateTable(self,row,column,value,candidateTable):
        self.updateRow(candidateTable,row,value)
        self.updateColumn(candidateTable,column,value)   
        self.updateBox(candidateTable,row,column,value)

    def updateRow(self,candidateTable,row,value):
        for x in candidateTable[row]:
            if x != 0 and x.count(value) == 1:
                x.remove(value)

    def updateColumn(self,candidateTable,column,value):
        for row in candidateTable:
            if row[column] != 0 and row[column].count(value) == 1:
                row[column].remove(value)

    def updateBox(self,candidateTable,row,column,value):
        topRow = getBoxTopLeft(row)
        topColumn = getBoxTopLeft(column)

        for x in range(topRow, topRow + 3):
            for y in range(topColumn, topColumn + 3):
                if candidateTable[x][y] != 0 and candidateTable[x][y].count(value) == 1:
                    candidateTable[x][y].remove(value)

    def solveTrivialCells(self, candidateTable):
        changeMade = False
        self.solveTrivialSingleCells(self.boardArray, candidateTable, changeMade)
        self.solveHiddenCells(self.boardArray, candidateTable, changeMade)

        if changeMade == True:
            self.solveTrivialCells(self.boardArray, candidateTable)

    def solveHiddenCells(self, candidateTable,changeMade):
        self.checkHiddenRows(candidateTable,changeMade)
        self.checkHiddenColumns(candidateTable,changeMade)
        self.checkHiddenBoxes(candidateTable,changeMade)

    def checkHiddenRows(self, candidateTable,changeMade):
        for i in range(0,9):
            missingValues = []
            for h in range(1,10):
                if self.boardArray[i].count(h) == 0:
                    missingValues.append(h)
            
            for value in missingValues:
                countOfValue = 0
                index = 0
                for k in range(0,9):
                    if candidateTable[i][k] != 0 and candidateTable[i][k].count(value) == 1:
                        countOfValue += 1
                        index = k
                if countOfValue == 1:
                    self.solveATrivialCell(i, index, candidateTable)
                    changeMade = True

    def checkHiddenColumns(self, candidateTable,changeMade):
        for column in range(0,9):
            self.checkHiddenColumn(candidateTable,changeMade,column)
        
    def checkHiddenColumn(self, candidateTable, changeMade, column):
        missingValues = self.findMissingColumnValues(column)

        for value in missingValues:        
            index = self.checkIfValueIsInOnlyOneCandidateList(column,value,candidateTable)
            if index != -1:
                self.solveATrivialCell(i, index, candidateTable)
                changeMade = True

    def checkHiddenBoxes(candidateTable,changeMade):
        for x in range(0,7,3):
            for y in range(0,7,3):
                self.checkHiddenBox(candidateTable,changeMade,x,y)
            
    def checkHiddenBox(candidateTable,changeMade,row,column):
        missingValues = self.findMissingBoxValues(row, column)

        for value in missingValues: 
            index = self.checkIfValueIsInOnlyOneBoxCandidateList(row,column,value,candidateTable)
            if index != -1:
                self.solveATrivialCell(i, index, candidateTable)
                changeMade = True


    def solveATrivialCell(self, row, column, candidateTable):
        self.boardArray[row][column] = candidateTable[row][column].pop()
        candidateTable[row][column] = []
        self.updateCandidateTable(row, column, self.boardArray[row][column], candidateTable)

    def findMissingColumnValues(self,column):
        columnList = []

        for row in self.boardArray:
            columnList.append(row[column])

        return self.findMissingValues(boxList)

    def findMissingBoxValues(self, row, column):
        boxList = []

        for x in range(row, row + 3):
            for y in range(column, column + 3):
                boxList.append(self.boardArray[x][y])
        
        return self.findMissingValues(boxList)
    
    def findMissingValues(self,list):
        for i in range(1,10):
            if list.count(i) == 0:
                missingValues.append(i)
        return missingValues

    def checkIfValueIsInOnlyOneCandidateList(self,column,value,candidateTable):
        countOfValue = 0
        index = 0
        for i in range(0,9):
                if candidateTable[i][column] != 0 and candidateTable[i][column].count(value) == 1:
                    countOfValue += 1
                    index = i

        if countOfValue == 1:
            return index
        return -1

    def checkIfValueIsInOnlyOneBoxCandidateList(row,column,value,candidateTable):
        countOfValue = 0
        index = 0

        for x in range(row, row + 3):
            for y in range(column, column + 3):
                if candidateTable[x][y] != 0 and candidateTable[i][column].count(value) == 1:
                    countOfValue += 1
                    index = i

        if countOfValue == 1:
            return index
        return -1

    def solveTrivialSingleCells(self, candidateTable, changeMade):
        for x in range(0, 9):
            for y in range(0, 9):
                if self.boardArray[x][y] == 0 and len(candidateTable[x][y]) == 1:
                    self.boardArray[x][y] = candidateTable[x][y].pop()
                    candidateTable[x][y] = []
                    self.updateCandidateTable(x, y, self.boardArray[x][y], candidateTable)
                    changeMade = True

    def getNextValueInList(self,list,value):
        index = list.index(value)

        if index == len(list) - 1:
            return -1
        return list[index + 1]
    