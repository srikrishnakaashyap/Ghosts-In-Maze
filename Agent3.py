from Agent2 import Agent2
from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import deepcopy
from heapq import heapify, heappop
import math


class Agent3:

    # Given the number of times a cell is visited, this function returns the penalty
    # that we need to add for the step. This function initially grows slowly until
    # the value reaches around 50. After which, this function grows
    # exponentially and penalty dominates the success rate and distance
    # in making the decision thereby breaking the wiggle.
    # Since wiggling is nice until 30-35 moves, this heuristic was chosen.
    def getPenalty(self, x):
        return x**2 / 5000

    # This is an iterative version of Agent 3. We moved from the recursive version
    # because our recursive version was throwing a maximum recursion depth.
    def agent3Iterative(
        self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)
    ):
        while True:
            visited[(currRow, currCol)] += 1

            # print(currRow, currCol)

            # If there is a ghost in the current cell we are in, then
            # we return False indicating the agents death
            if (currRow, currCol) in ghostMap:
                print("1")
                return False, grid, (currRow, currCol), ghostMap

            # If the above condition fails and we reach the destination,
            # we return True
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]

            # This is our heap datastructure in which we store the tuples.
            # The first value in the tuple contains our heuristic value
            # and the second value contains the step that we are taking.
            d = []

            # Utility.printMaze(grid)

            # Traversing the four directions
            for i in range(4):
                newRow = currRow + rows[i]
                newCol = currCol + cols[i]

                # If we have reached the destination, we return True
                if newRow == len(grid) - 1 and newCol == len(grid[0]) - 1:
                    return True, grid, (newRow, newCol), ghostMap

                # If the new cell is valid and the ghost doesnt
                # exist in the new cell, then we consider the cell
                if (
                    0 <= newRow < len(grid)
                    and 0 <= newCol < len(grid[0])
                    and grid[newRow][newCol] % 2 == 0
                    and (newRow, newCol) not in ghostMap
                ):

                    # We run agent 2 from the new cell for 10 iterations and
                    # calculate the success rate.
                    successRate = 0
                    for j in range(10):
                        a2 = Agent2()
                        successRate += a2.agent2(
                            newRow, newCol, deepcopy(grid), path, deepcopy(ghostMap)
                        )[0]

                    # Since we get the success rate, we can determine the
                    # failure rate.
                    failureRate = 10 - successRate
                    penality = self.getPenalty(visited[(newRow, newCol)])
                    distance = path[newRow][newCol][2]

                    # If the penality doesnt overdominate our heuristic,
                    # we append this into the heap as one of the potential choices.
                    if penality < 100:

                        # We append the Failure Rate + penality + distance as our decision heuristic
                        # and the new coordinates.

                        # Our aim is to minimize this value
                        d.append(
                            (
                                failureRate + penality + distance,
                                (newRow, newCol),
                            )
                        )
                    # print(d)

            # Utility.printMaze(grid)

            # We heapify the heap and if there are no elements in the heap,
            # then we choose the shortest path thereby making some progress.
            heapify(d)
            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[1]
            else:
                newAgentPosition = (
                    path[currRow][currCol][0],
                    path[currRow][currCol][1],
                )

            # We iterate through every ghost present in the ghostMap
            # and move the ghost by one step.
            newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)

                    # If we move ghost into the cell containing the agent,
                    # then we return false indicating the agents death
                    if newAgentPosition == newPosition:
                        print("2")
                        return False, grid, newPosition, ghostMap

                    newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = deepcopy(newGhostMap)

            # Utility.printMaze(grid)
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]
            print(currRow, currCol)

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

        ghostMap = deepcopy(self.newGhostMap)

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
