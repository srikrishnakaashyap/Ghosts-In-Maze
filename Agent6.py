from Agent4 import Agent4
from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import copy
from heapq import heapify, heappop
import math


class Agent6:
    def getPenalty(self, x):
        return x**2 / 5000

    def agent6(self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)):
        while True:
            visited[(currRow, currCol)] += 1

            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]
            d = []
            Utility.printMaze(grid)
            for i in range(4):
                newRow = currRow + rows[i]
                newCol = currCol + cols[i]
                if newRow == len(grid) - 1 and newCol == len(grid[0]) - 1:
                    return True, grid, (newRow, newCol), ghostMap
                if (
                    0 <= newRow < len(grid)
                    and 0 <= newCol < len(grid[0])
                    and grid[newRow][newCol] == 0
                ):

                    successrate = 0
                    iterations = 10
                    for j in range(10):
                        successrate += self.agent4.agent4(
                            newRow,
                            newCol,
                            copy(grid),
                            path,
                            copy(ghostMap),
                            copy(visited),
                        )[0]

                    failureRate = iterations - successrate
                    distance = path[newRow][newCol][2]
                    penality = self.getPenalty(visited[(newRow, newCol)])

                    d.append(
                        (
                            failureRate + penality + distance,
                            (newRow, newCol),
                        )
                    )

            heapify(d)

            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[1]
            else:
                newAgentPosition = (currRow, currCol)

            self.newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    if newAgentPosition == newPosition:
                        print("2")
                        return False, grid, newPosition, ghostMap

                    self.newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = copy(self.newGhostMap)

            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]
            print(currRow, currCol)

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        self.agent4 = Agent4()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        Utility.printMaze(grid)

        visited = defaultdict(int)

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = self.agent6(0, 0, grid, path, ghostMap, visited)

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        # print(finalAgentPosition)

        # print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent6 = Agent6()

    agent6.findPath(10, 5)
