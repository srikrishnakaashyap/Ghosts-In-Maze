from turtle import distance
from xmlrpc.client import boolean
from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import copy


class Agent2:
    def computePath(self, row, col, path):

        pathMap = defaultdict(boolean)

        while True:
            if row == len(path) - 1 and col == len(path[0]) - 1:
                break
            pathMap[(row, col)] = False
            newPos = path[row][col]
            row = newPos[0]
            col = newPos[1]

        return pathMap

    def isGhostPresentInPath(self, ghostMap, currPathSet, path, currRow, currCol):
        distance = len(currPathSet)
        isGhostPresent = False
        for key, value in ghostMap.items():

            if key in currPathSet:
                isGhostPresent = True
                distance = min(
                    distance, path[key[0]][key[1]][2] - path[currRow][currCol][2]
                )

        return isGhostPresent, distance

    def replan(self, grid, path, ghostMap, currPathSet, currRow, currCol):
        nextRow = path[currRow][currCol][0]
        nextCol = path[currRow][currCol][1]
        rows = [0, 0, -1, 1]
        cols = [1, -1, 0, 0]
        for i in range(4):
            newrow, newcol = currRow + rows[i], currCol + cols[i]
            if (newrow, newcol == nextRow, nextCol):
                continue

    def agent2(self, grid, path, ghostMap):

        #  Computing the path after every agent step

        currPathMap = self.computePath(0, 0, path)
        currRow = 0
        currCol = 0

        while True:
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                break

            if self.isGhostPresentInPath(ghostMap, currPathMap):
                # Replan
                pass
            else:
                newAgentPosition = path[currRow][currCol]
                currPathMap[(currRow, currCol)] = True
                currRow = newAgentPosition[0]
                currCol = newAgentPosition[1]

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

                ghostMap = copy(self.newGhostMap)

        return True, grid, (currRow, currCol), ghostMap

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        result, finalGrid, finalAgentPosition, finalGhostPosition = self.agent2(
            grid, path, ghostMap
        )

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        print(finalAgentPosition)

        print(finalGhostPosition)


if __name__ == "__main__":
    agent2 = Agent2()

    agent2.findPath(5, 1)
