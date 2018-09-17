from ValidationChecker import getBoxTopLeft
import copy

class Solver:

    def __init__(self, boardArray, validationChecker):
        self.boardArray = boardArray
        self.validationChecker = validationChecker

    def solvePuzzle(self):
        valid = self.validationChecker.checkInitialValidity(self.boardArray)
        if not valid:
            print("Invalid board!")
            return
        candidateTable = self.buildCandidateTable()
        self.solveTrivialCells(candidateTable)
        initialBoard = copy.deepcopy(self.boardArray)
        return self.solvePuzzleRecursively(0,0, "forward", initialBoard,candidateTable)

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
    
        if self.boardArray[row][column] == 9: 
            self.boardArray[row][column] = 0
            return self.solvePuzzleRecursively(row,column - 1, "backwards", initialBoard,candidateTable)

        self.boardArray[row][column]+= 1
        while not self.validationChecker.checkValidity(self.boardArray,row,column):
            self.boardArray[row][column]+= 1
            if self.boardArray[row][column] == 10:
                self.boardArray[row][column] = 0
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
            if self.validationChecker.checkValidity(self.boardArray,x,y):
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
        changeMade = self.solveTrivialSingleCells(candidateTable)
        changeMade = True if self.solveHiddenCells(candidateTable) else changeMade

        if changeMade == True:
            self.solveTrivialCells(candidateTable)

    def solveHiddenCells(self, candidateTable):
        changeMade = self.checkHiddenRows(candidateTable)
        changeMade = True if self.checkHiddenColumns(candidateTable) else changeMade
        changeMade = True if self.checkHiddenBoxes(candidateTable) else changeMade
        return changeMade

    def checkHiddenRows(self, candidateTable):
        changeMade = False
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
                    self.solveATrivialCell(i, index, value, candidateTable)
                    changeMade = True

        return changeMade

    def checkHiddenColumns(self, candidateTable):
        changeMade = False
        for column in range(0,9):
            changeMade = True if self.checkHiddenColumn(candidateTable,column) else changeMade
        return changeMade
        
    def checkHiddenColumn(self, candidateTable, column):
        changeMade = False
        missingValues = self.findMissingColumnValues(column)

        for value in missingValues:        
            index = self.checkIfValueIsInOnlyOneCandidateList(column,value,candidateTable)
            if index != -1:
                self.solveATrivialCell(index, column, value, candidateTable)
                changeMade = True

        return changeMade

    def checkHiddenBoxes(self,candidateTable):
        changeMade = False
        for x in range(0,7,3):
            for y in range(0,7,3):
                changeMade = True if self.checkHiddenBox(candidateTable,x,y) else changeMade
        return changeMade
            
    def checkHiddenBox(self,candidateTable,row,column):
        changeMade = False

        missingValues = self.findMissingBoxValues(row, column)

        for value in missingValues: 
            index = self.checkIfValueIsInOnlyOneBoxCandidateList(row,column,value,candidateTable)
            if index != -1:
                self.solveATrivialCell(index[0], index[1], value, candidateTable)
                changeMade = True

        return changeMade

    def solveATrivialCell(self, row, column, value, candidateTable):
        self.boardArray[row][column] = value
        candidateTable[row][column] = []
        self.updateCandidateTable(row, column, self.boardArray[row][column], candidateTable)

    def findMissingColumnValues(self,column):
        columnList = []

        for row in self.boardArray:
            columnList.append(row[column])

        return self.findMissingValues(columnList)

    def findMissingBoxValues(self, row, column):
        boxList = []

        for x in range(row, row + 3):
            for y in range(column, column + 3):
                boxList.append(self.boardArray[x][y])
        
        return self.findMissingValues(boxList)
    
    def findMissingValues(self,list):
        missingValues = []

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

    def checkIfValueIsInOnlyOneBoxCandidateList(self,row,column,value,candidateTable):
        countOfValue = 0
        index = []

        for x in range(row, row + 3):
            for y in range(column, column + 3):
                if candidateTable[x][y] != 0 and candidateTable[x][y].count(value) == 1:
                    countOfValue += 1
                    index.append(x)
                    index.append(y)

        if countOfValue == 1:
            return index
        return -1

    def solveTrivialSingleCells(self, candidateTable):
        changeMade = False

        for x in range(0, 9):
            for y in range(0, 9):
                if self.boardArray[x][y] == 0 and len(candidateTable[x][y]) == 1:
                    self.boardArray[x][y] = candidateTable[x][y].pop()
                    candidateTable[x][y] = []
                    self.updateCandidateTable(x, y, self.boardArray[x][y], candidateTable)
                    changeMade = True
        return changeMade

    def getNextValueInList(self,list,value):
        index = list.index(value)

        if index == len(list) - 1:
            return -1
        return list[index + 1]
    