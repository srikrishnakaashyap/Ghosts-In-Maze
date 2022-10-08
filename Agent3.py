from Agent2 import Agent2
from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import copy
from heapq import heapify, heappop


class Agent3:

    # def isGhostPresent(self, ghostMap, currRow, currCol):
    #     ghostDirection = set()
    #     for i in range(-3, 4):
    #         for j in range(-3, 4):
    #             if (currRow+i,currCol+j) in ghostMap:
    #                 ghostDirection.add((i,j))
    #     isGhostPresent = False

    #     return isGhostPresent, distance

    # def computePath(self, row, col, path):

    #     pathMap = defaultdict(bool)

    #     while True:
    #         if row == len(path) - 1 and col == len(path[0]) - 1:
    #             break
    #         pathMap[(row, col)] = False
    #         newPos = path[row][col]
    #         row = newPos[0]
    #         col = newPos[1]

    #     return pathMap

    # def modifiedAgent2(self, currRow, currCol, grid, path, ghostMap):

    #     #  Computing the path after every agent step

    #     currPathMap = self.computePath(currRow, currCol, path)
    #     while True:
    #         if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
    #             break

    #         isGhostPresent, direction = self.isGhostPresent(
    #             ghostMap, currRow, currCol
    #         )

    #         if isGhostPresent:
    #             currRow, currCol, currPathMap = self.replan(
    #                 grid, path, ghostMap, currPathMap, currRow, currCol, distance
    #             )
    #             self.newGhostMap = defaultdict(int)
    #             for key, value in ghostMap.items():

    #                 g = value
    #                 while g > 0:
    #                     row = key[0]
    #                     col = key[1]

    #                     newPosition = Utility.moveGhost(row, col, grid)
    #                     if (currRow, currCol) == newPosition:
    #                         return False, grid, (currRow, currCol), ghostMap

    #                     self.newGhostMap[newPosition] += 1

    #                     g -= 1

    #             ghostMap = copy(self.newGhostMap)
    #         else:
    #             newAgentPosition = path[currRow][currCol]
    #             currPathMap[(currRow, currCol)] = True
    #             currRow = newAgentPosition[0]
    #             currCol = newAgentPosition[1]

    #             self.newGhostMap = defaultdict(int)
    #             for key, value in ghostMap.items():

    #                 g = value
    #                 while g > 0:
    #                     row = key[0]
    #                     col = key[1]

    #                     newPosition = Utility.moveGhost(row, col, grid)
    #                     if newAgentPosition[:2] == newPosition:
    #                         return False, grid, (currRow, currCol), ghostMap

    #                     self.newGhostMap[newPosition] += 1

    #                     g -= 1

    #             ghostMap = copy(self.newGhostMap)

    #     return True, grid, (currRow, currCol), ghostMap

    def agent3(self, currRow, currCol, grid, path, ghostMap):

        print(currRow, currCol)

        if (currRow, currCol) in ghostMap:
            return False

        if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
            return True

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]

        d = []

        for i in range(4):
            newRow = currRow + rows[i]
            newCol = currRow + cols[i]
            if (
                0 <= newRow < len(grid)
                and 0 <= newCol < len(grid[0])
                and grid[newRow][newCol] % 2 != 1
            ):
                successRate = 0
                for j in range(10):
                    successRate += self.agent2.agent2(
                        newRow, newCol, grid, path, ghostMap
                    )[0]

                # print(newRow, newCol)
                d.append((-successRate, path[newRow][newCol][2], (newRow, newCol)))

        heapify(d)
        # print(d)
        direction = heappop(d)
        newAgentPosition = direction[2]

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

        return self.agent3(
            newAgentPosition[0], newAgentPosition[1], grid, path, ghostMap
        )

    def findPath(self, gridSize, numberOfGhosts):
        self.mg = MazeGeneration()

        self.agent2 = Agent2()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        # Utility.printMaze(grid)

        result, finalGrid, finalAgentPosition, finalGhostPosition = self.agent3(
            0, 0, grid, path, ghostMap
        )

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        print(finalAgentPosition)

        print(finalGhostPosition)


if __name__ == "__main__":

    agent3 = Agent3()

    agent3.findPath(51, 1)
