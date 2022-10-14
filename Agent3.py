from Agent2 import Agent2
from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import copy
from heapq import heapify, heappop
import math


class Agent3:
    def getPenalty(self, x):
        return x**2 / 5000

    # Try Failure Rate + distance + penality
    def agent3Iterative(
        self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)
    ):
        while True:
            visited[(currRow, currCol)] += 1

            # print(currRow, currCol)

            if (currRow, currCol) in ghostMap:
                print("1")
                return False, grid, (currRow, currCol), ghostMap

            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]
            d = []

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
                    successRate = 0
                    for j in range(10):
                        successRate += self.agent2.agent2(
                            newRow, newCol, copy(grid), copy(path), copy(ghostMap)
                        )[0]

                    failureRate = 10 - successRate
                    penality = self.getPenalty(visited[(newRow, newCol)])
                    distance = path[newRow][newCol][2]

                    if penality < 100:
                        d.append(
                            (
                                failureRate + penality + distance,
                                (newRow, newCol),
                            )
                        )
                    # print(d)

            heapify(d)
            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[1]
            else:
                newAgentPosition = (
                    path[currRow][currCol][0],
                    path[currRow][currCol][1],
                )

            newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    if newAgentPosition == newPosition:
                        print("2")
                        return False, grid, newPosition, ghostMap

                    newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = copy(newGhostMap)

            print(currRow, currCol, ghostMap)
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

    def agent3Recursive(self, currRow, currCol, grid, path, ghostMap, visited):

        visited[(currRow, currCol)] += 1

        print(currRow, currCol)

        if (currRow, currCol) in ghostMap:
            print("1")
            return False, grid, (currRow, currCol), ghostMap

        if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
            return True, grid, (currRow, currCol), ghostMap

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]
        d = [
            (-self.getPenalty(visited[(currRow, currCol)]), (currRow, currCol)),
        ]

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
                successRate = 0
                for j in range(10):
                    successRate += self.agent2.agent2(
                        newRow, newCol, grid, path, ghostMap
                    )[0]

                d.append(
                    (
                        -(successRate - self.getPenalty(visited[(newRow, newCol)])),
                        (newRow, newCol),
                    )
                )
                # print(d)

        heapify(d)
        # print(d, currRow, currCol)
        direction = heappop(d)
        newAgentPosition = direction[1]

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

        return self.agent3(
            newAgentPosition[0], newAgentPosition[1], grid, path, ghostMap, visited
        )

    def findPath(self, gridSize, numberOfGhosts):
        self.mg = MazeGeneration()

        self.agent2 = Agent2()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        # Utility.printMaze(grid)

        visited = defaultdict(int)

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = self.agent3Iterative(0, 0, grid, path, ghostMap, visited)

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        # print(finalAgentPosition)

        # print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent3 = Agent3()

    agent3.findPath(51, 50)
