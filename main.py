import time
from enum import Enum
from copy import deepcopy

class Timer :
    def __init__(self):
        self.start = time.perf_counter()

    def __del__(self):
        self.end = time.perf_counter()
        duration = self.end - self.start
        print(f"Duration Run Time = {duration:.20f} Sec")

class Board:
    def __init__(self, board=None, level=None, functionValue=None):
        self.board = board
        self.level = level
        self.functionValue = functionValue

class ProcessesBoard :

    @staticmethod
    def getControllerTilePosition(board):
        numberTiles = len(board.board)
        for i in range(numberTiles):
            if not str(board.board[i]).isnumeric():
                return i

    @staticmethod
    def direction(position):
        directions = [Directions.right, Directions.left, Directions.up, Directions.down]
        if position % 3 == 0 :
            directions.remove(Directions.left)
        if position % 3 == 2:
            directions.remove(Directions.right)
        if position % 3 > 2:
            directions.remove(Directions.down)
        if position / 3 < 1:
            directions.remove(Directions.up)
        if position / 3 >= 2:
            directions.remove(Directions.down)
        return directions


    @staticmethod
    def __move(board, directions, currentPosition):
        numberMoved = len(directions); children = []
        for move in range(numberMoved):
            """
                NOTS:   
                    - We Use direction.value Because Comparison Numbers Faster Comparison Text
                    - User deepcopy to set memory location point to difference location (Change In Temp Not Apply in board) 
            """

            if directions[move].value == 1: # up
                # position - 3
                temp = deepcopy(board)
                temp.board[currentPosition], temp.board[currentPosition - 3] = temp.board[currentPosition - 3], temp.board[currentPosition]
                children.append(temp)



            if directions[move].value == 2 : # Down
                # position + 3
                temp = deepcopy(board)
                temp.board[currentPosition], temp.board[currentPosition + 3] = temp.board[currentPosition + 3], temp.board[currentPosition]
                children.append(temp)



            if directions[move].value == 3: # right
                # position + 1
                temp = deepcopy(board)
                temp.board[currentPosition], temp.board[currentPosition + 1] = temp.board[currentPosition + 1], temp.board[currentPosition]
                children.append(temp)


            if directions[move].value == 4: # left
                # position - 1
                temp = deepcopy(board)
                temp.board[currentPosition], temp.board[currentPosition - 1] = temp.board[currentPosition - 1], temp.board[currentPosition]
                children.append(temp)

        return children


    def prepareNextLevel(self, board):
        position = self.getControllerTilePosition(board)
        directions = self.direction(position)
        possibleDirections = self.__move(board, directions, position)
        return possibleDirections




class Directions(Enum) :
    up = 1; down = 2; right =3; left = 4


class Puzzle(ProcessesBoard):
    def __init__(self, initState, goal=None):
        self.initState = initState
        self.goal = goal if goal is not None else [1, 2, 3, 4, 5, 6, 7, 8, '-']
        self.numberTiles = len(self.initState)
        self.path = []; self.station = []
        self.numberSteps = 0
        self.lastLevel = 0

    def __totalTime(self, node : Board) -> int:
        return self.heuristic(node.board) + node.level

    def showBoard(self, board):
        for i in range(self.numberTiles):
            if (i + 1) % 3 != 0:
                print(board.board[i], end=' | ')
            else :
                print(board.board[i])
                print("----------")
        print("\n====================================\n")


    @staticmethod
    def ifSolved(board , goal) -> bool:
        tiles = len(board.board)
        for tile in range(tiles):
            if board.board[tile] != goal[tile]:
                return False
        return True


    def nextBoard(self, levelElement):
        siblingInfo = {}
        for idBoard, board in enumerate(levelElement):
            siblingInfo.update({board: self.__totalTime(board)})
        return min(siblingInfo, key=siblingInfo.get)

    def heuristic(self, board, goal=None):
        counter = 0
        if goal is None: goal = self.goal
        for i in range(self.numberTiles):
            if board[i] != goal[i] and board[i] != '-':
                counter += 1
        return counter



    def solver(self):
        levels = []
        root = Board(self.initState, self.lastLevel, 0)

        root.functionValue = self.__totalTime(root)

        self.station.append(root)
        levels.append([])
        levels[-1].append(root)



        while True:
            currentBoard = self.station[0]

            self.showBoard(currentBoard)
            '''
                * Why We Use IfSolved Method Not Heuristic Method ?
                    ifSolver Is Faster Because we Not need to check to all values in board
                    we break loop Just What It Becomes value tail in board not equal value tail in goal board
                Not: Use Timer class To Make Sure (And Test In Worst Case
            '''
            if Puzzle.ifSolved(currentBoard, self.goal): break


            # Get Next Level
            nextLevels = self.prepareNextLevel(currentBoard)
            levels.append(nextLevels)
            self.lastLevel += 1

            # Set Level For Each Board
            for node in levels[-1]:
                node.level = self.lastLevel
                self.station.append(node)

            # Get Next Node

            self.path.append([self.nextBoard(levels[-1])])
            del self.station[0]
            time.sleep(1)


play = Puzzle([
                    1, 2, 3,
                    4, '-', 6,
                    7, 5, 8
])
# play = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, '-'])
play.solver()
