class Sudoku:
    def __init__(self, matrix):
        self.matrix = matrix
    def __str__(self):
        PrintableSudoku = ""
        for row in self.matrix:
            for ColumnElement in row:
                PrintableSudoku += str(ColumnElement) + " "
            PrintableSudoku += '\n' 
        return PrintableSudoku
    def BackTrackingIsMovePossible(self, y, x, n):
        for i in range(0,9):
            if self.matrix[y][i] == n:
                return False
        for i in range(0,9):
            if self.matrix[i][x] == n:
                return False
        x0 = (x//3)*3
        y0 = (y//3)*3
        for i in range(0,3):
            for j in range(0,3):
                if self.matrix[y0+i][x0+i] == n:
                    return False
        return True
    def BackTrackingSolve(self):
        for row in range(9):
            for column in range(9):
                if(self.matrix[row][column] == 0):
                    for n in range(1,10):
                        if self.BackTrackingIsMovePossible(row,column,n):
                            self.matrix[row][column] = n
                            self.solve()
                            self.matrix[row][column] = 0
                    return
        print(self)
        input("More?")