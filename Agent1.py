from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import deepcopy
import seaborn as sns
import matplotlib.pylab as plt
import time

sns.set_theme(style="white")


class Agent1:
    def prepareGrid(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    grid[i][j] = 2
                if grid[i][j] > 1:
                    grid[i][j] = 4

        return grid

    def agent1(self, grid, path, ghostMap, ax=None, cbar_ax=None):
        currRow = 0
        currCol = 0

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # plotGrid = self.prepareGrid(copy(grid))
        # plotGrid[currRow][currCol] = 6
        # im = sns.heatmap(plotGrid, linewidth=0.5)
        # plt.show(block=False)
        # plt.pause(1)

        while True:
            # print(currRow, currCol)
            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                break

            # plotGrid = self.prepareGrid(copy(grid))
            # plotGrid[currRow][currCol] = 6
            # # fig.canvas.flush_events()
            # # fig.clf()
            # # plt.clf()
            # plt.gcf().canvas.flush_events()
            # sns.heatmap(ax=ax, data=plotGrid, cbar_ax=cbar_ax, linewidth=0.5)

            # # plt.clf()
            # # plt.draw()
            # plt.pause(0.1)

            newAgentPosition = path[currRow][currCol]
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            self.newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    # print(newAgentPosition[:2], newPosition)
                    if newAgentPosition[:2] == newPosition:
                        return False, grid, (currRow, currCol), ghostMap

                    self.newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = deepcopy(self.newGhostMap)

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

        # Utility.printMaze(grid)

        result, finalGrid, finalAgentPosition, finalGhostPosition = self.agent1(
            grid, path, ghostMap
        )

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        print(finalAgentPosition)

        print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent1 = Agent1()

    agent1.findPath(51, 50)
