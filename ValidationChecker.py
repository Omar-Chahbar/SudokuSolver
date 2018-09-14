class ValidationChecker:

    def checkValidity(self,board, row, column):
        value = board[row][column]
        if board[row].count(value) > 1:
            return False
        if not self.validColumn(board,column,value):
            return False
        if not self.validBox(board,row,column,value):
            return False
        return True

    def validColumn(self,board,column,value):
        columnList = []
        for row in board:
            columnList.append(row[column])
        return columnList.count(value) == 1

    def validBox(self,board,row,column,value):
        boxTopRow = getBoxTopLeft(row)
        boxTopColumn = getBoxTopLeft(column)

        box = []
        for r in range (boxTopRow,boxTopRow + 3):
            for c in range (boxTopColumn,boxTopColumn + 3):
                box.append(board[r][c])
        
        return box.count(value) == 1

    def checkInitialValidity(self, board):
        if not self.InitialRowsValid(board):
            return False
        if not self.InitialColumnsValid(board):
            return False
        if not self.InitialBoxesValid(board):
            return False
        return True

    def InitialRowsValid(self, board):
        for row in board:
            if self.hasDuplicates(row):
                return False
        return True  

    def InitialColumnsValid(self, board):
        columnList = []
        for column in range (0,9):
            for row in board:
                columnList.append(row[column])
            if self.hasDuplicates(columnList):
                return False 
            columnList.clear()
        return True

    def InitialBoxesValid(self, board):
        box = []
        for r in range(0,7,3):
            for c in range(0,7,3):
                box = self.buildBox(board,r,c)
                if self.hasDuplicates(box):
                    return False
        return True

    def hasDuplicates(self, list):
        difference = len(list) - len(set(list))
        if difference != list.count(0) - 1 and difference != 0:
            return True
        return False

    def buildBox(self,board,row,column):
        box = []

        for r in range(row, row + 3):
            for c in range(column, column + 3):
                box.append(board[r][c])
        return box

def getBoxTopLeft(index):
    if index >= 6:
        return 6
    elif index >= 3:
        return 3
    return 0