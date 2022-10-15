from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import deepcopy

# import seaborn as sns
# import matplotlib.pylab as plt
import time

# sns.set_theme(style="white")


class Agent1:

    # This is a utility function that is used to visualize the maze.
    # This function doesn't have any significance for the
    # agent implementation
    def prepareGrid(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    grid[i][j] = 2
                if grid[i][j] > 1:
                    grid[i][j] = 4

        return grid

    # Given the grid, path(precomputed matrix of the distance and the next cell),
    # and the ghostMap that stores the current position of
    # ghosts, this function performs the Agent 1 steps
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

        # This loop runs till either we reach the destination,
        # or get eaten by the ghost.
        while True:
            # print(currRow, currCol)
            # If there is a ghost in the current cell we are in, then
            # we return False indicating the agents death
            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            # If the above condition fails and we reach the destination,
            # we break out of the loop.
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

            # The next position that the agent needs to go to is in the
            # current index of the path array.
            # Hence, we find the next position.
            newAgentPosition = path[currRow][currCol]
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

            # If the cell into which the agent moved already has a ghost in it
            # we return false.
            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            # We iterate through every ghost present in the ghostMap
            # and move the ghost by one step.
            self.newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    # print(newAgentPosition[:2], newPosition)

                    # If we move ghost into the cell containing the agent,
                    # then we return false indicating the agents death
                    if newAgentPosition[:2] == newPosition:
                        return False, grid, (currRow, currCol), ghostMap

                    self.newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = deepcopy(self.newGhostMap)

        # If we break out of the loop, then this indicates that we have
        # reached the destination and we return True
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
