from Agent4 import Agent4
from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import deepcopy
from heapq import heapify, heappop
import math


class Agent6:
    # This is a takeaway from Agent 3. We use the penalty
    # that grows slowly initially and grows exponentially
    # with the increase in its values so that we dont
    # visit the same cell again and again.
    def getPenalty(self, x):
        return x**2 / 5000

    def agent6(self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)):
        while True:
            # We update the number of times we visit the cell
            # in the hashmap
            visited[(currRow, currCol)] += 1

            # If there is a ghost in the current cell we are in, then
            # we return False indicating the agents death
            if (currRow, currCol) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            # If the above condition fails and we reach the destination,
            # we return true
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]
            d = []
            # Utility.printMaze(grid)

            # Traversing the neighbours
            for i in range(4):
                newRow = currRow + rows[i]
                newCol = currCol + cols[i]

                # If the neighbour is the destination, we return True
                if newRow == len(grid) - 1 and newCol == len(grid[0]) - 1:
                    return True, grid, (newRow, newCol), ghostMap

                # If the new cell is valid and the ghost doesnt
                # exist in the new cell, then we consider the cell
                if (
                    0 <= newRow < len(grid)
                    and 0 <= newCol < len(grid[0])
                    and grid[newRow][newCol] == 0
                ):

                    # We run agent 4 from the new cell for 10 iterations and
                    # calculate the success rate.
                    successrate = 0
                    iterations = 10
                    for j in range(10):
                        successrate += self.agent4.agent4(
                            newRow,
                            newCol,
                            deepcopy(grid),
                            path,
                            deepcopy(ghostMap),
                            deepcopy(visited),
                        )[0]

                    # Since we get the success rate, we can determine the
                    # failure rate.
                    failureRate = iterations - successrate
                    distance = path[newRow][newCol][2]
                    penality = self.getPenalty(visited[(newRow, newCol)])

                    # We append the Failure Rate + penality + distance as our decision heuristic
                    # and the new coordinates.

                    # Our aim is to minimize this value
                    d.append(
                        (
                            failureRate + penality + distance,
                            (newRow, newCol),
                        )
                    )

            heapify(d)

            # If the heap is empty, then staying at the same cell is taken to be a
            # desired move
            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[1]
            else:
                newAgentPosition = (currRow, currCol)

            self.newGhostMap = defaultdict(int)
            # We iterate through the ghostMap and move the ghosts
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

                    self.newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = deepcopy(self.newGhostMap)

            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]
            print(currRow, currCol)

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        self.agent4 = Agent4()

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
        ) = self.agent6(0, 0, grid, path, ghostMap, visited)

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        # print(finalAgentPosition)

        # print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent6 = Agent6()

    agent6.findPath(51, 5)
