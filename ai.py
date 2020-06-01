#from tetris import join_matrixes, check_collision, remove_row
from copy import deepcopy

from pip._vendor.msgpack.fallback import xrange


class AI(object):

    weight1 = 0
    weight2 = 10
    weight3 = 0

    def __init__(self):
        self.columnHeights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def trackHeight(self, stone, stone_x, board, array):
        #print "trackHeight array is immediately ", array
        #print "------------------"
        #for r in board:
         #   print r, '\n'
        #print "------------------"
        span = len(stone[0])
        for n in range (stone_x, stone_x+span):
            i = -1
            for x in board:
                i += 1
                if x[n]:
                    array[n] = 22-i
                    break
        #print array
        return array
        

    def check_collision(self, board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[ cy + off_y ][ cx + off_x ]:
                        return True
                except IndexError:
                    return True
        return False

    def join_matrixes(self, mat1, mat2, mat2_off):
        off_x, off_y = mat2_off
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                mat1[cy+off_y-1][cx+off_x] += val
        return mat1

    def remove_row(self, board, row):
        del board[row]
        return [[0 for i in xrange(10)]] + board

    def rotate(self, shape):
        return [ [ shape[y][x]
                        for y in xrange(len(shape)) ]
                for x in xrange(len(shape[0]) - 1, -1, -1) ]

    def snap(self, stone, board, column):
        stone_y = 0
        finished = False
        while not finished:
            stone_y += 1
            if self.check_collision(board, stone,(column, stone_y)):
                finished = True
                new_board = self.join_matrixes(board, stone,(column, stone_y))
                #print "--------------------------------"
                #for r in new_board:
                #    print r, '\n'
                #print "--------------------------------"
                tempHeights = self.trackHeight(stone, column, new_board, deepcopy(self.columnHeights))
                cleared_rows = 0
                level = stone_y
                for row in range(len(stone)):
                    if 0 not in new_board[level]:
                        new_board = self.remove_row(new_board, level)
                        cleared_rows += 1
                        level += 1
                if cleared_rows > 0:
                    tempHeights = self.clearHeight(cleared_rows, tempHeights)
        return new_board, cleared_rows, tempHeights, stone_y

    def h(self, board, stone):
       # print "stone ", stone
        best_score = 10000
        best_loc = [0,0] # [stone's x coordinate, stone's rotation]
        best_pretend_heights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for rotation in range(4):
            stone = self.rotate(stone)
            span = len(stone[0])
            for column in range(10-span):
                # Checks first to see if this would be an immediate game over
                if not self.check_collision(board, stone, (column, 0)):
                # Places stone in given position, creates new board based on position
                    new_board, cleared_lines, pretendHeights, height= self.snap(stone, deepcopy(board), column)
                    #print "pretendHeights is now ", pretendHeights
                    # Evaluates heuristic based on new board
                   # print "--------------------------------------------------------------"
                    #for r in new_board:
                     #  print r, '\n'
                    #print "--------------------------------------------------------------"
                    score = self.weight1 * self.get_holes(new_board, pretendHeights, stone, column) + self.weight2 * self.total_height(pretendHeights) - self.weight3 * cleared_lines
                    #print "score= ", score, "movement= ", column, "rotation= ", rotation
                    #print "score= ", score, "rotated ", rotation+1, " times"
                    if score < best_score:
                        best_score = score
                        best_pretend_heights = pretendHeights
                        best_loc = [column, rotation]
        self.columnHeights = best_pretend_heights
        print ("BEST MOVE: ", best_loc)
        return best_loc


    def total_height(self, array):
        total = 0
        for n in array: 
            total += n
        return total
    
    def get_holes(self, board, heights, stone, stone_x):
        total = 0
        span = len(stone[0])
        for n in range (stone_x, stone_x+span):
            print ("n= ", n)
            i = 1
            while not board[21-heights[n] + i][n]:
                print ("heights[n] ", heights[n])
                print ("i= ", i)
                total += 1
                i += 1
        return total
                
        
    def clearHeight(self, cleared_rows, array):
        for n in range (0, len(self.columnHeights)):
            array[n] -= cleared_rows
        return array

    def printHeight(self):
        print(self.columnHeights)
