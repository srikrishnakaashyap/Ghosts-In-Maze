from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import copy


class Agent1:
    def agent1(self, grid, path, ghostMap):
        currRow = 0
        currCol = 0

        while True:
            # print(currRow, currCol)
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                break

            newAgentPosition = path[currRow][currCol]
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

            self.newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    if newAgentPosition == newPosition:
                        return False, grid, (currRow, currCol), ghostMap

                    self.newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = copy(self.newGhostMap)

        return True, grid, (currRow, currCol), ghostMap

    def findPath(self, gridSize, numberOfGhosts):
        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)
        # grid = [
        #     [0, 1, 1, 0, 0],
        #     [0, 0, 1, 1, 0],
        #     [0, 0, 0, 0, 0],
        #     [0, 0, 1, 0, 1],
        #     [1, 0, 0, 0, 0],
        # ]

        # path = [
        #     [(1, 0), -1, -1, (0, 4), (1, 4)],
        #     [(2, 0), (2, 1), -1, -1, (2, 4)],
        #     [(3, 0), (3, 1), (2, 3), (3, 3), (2, 3)],
        #     [(3, 1), (4, 1), -1, (4, 3), -1],
        #     [-1, (4, 2), (4, 3), (4, 4), -1],
        # ]

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        result, finalGrid, finalAgentPosition, finalGhostPosition = self.agent1(
            grid, path, ghostMap
        )

        print(result)

        # Utility.printMaze(finalGrid)

        print(finalAgentPosition)

        print(finalGhostPosition)


if __name__ == "__main__":

    agent1 = Agent1()

    agent1.findPath(51, 25)
