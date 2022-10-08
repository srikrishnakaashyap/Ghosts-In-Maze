from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import copy


class Agent2:
    def computePath(self, row, col, path):

        pathMap = defaultdict(bool)

        while True:
            if row == len(path) - 1 and col == len(path[0]) - 1:
                break
            pathMap[(row, col)] = False
            newPos = path[row][col]
            # print("NEW POS", newPos)
            row = newPos[0]
            col = newPos[1]

        return pathMap

    def isGhostPresentInPath(self, ghostMap, currPathMap, path, currRow, currCol):
        distance = len(currPathMap)
        isGhostPresent = False

        for key, value in ghostMap.items():

            if key in currPathMap:
                isGhostPresent = True
                ghostDistance = path[currRow][currCol][2] - path[key[0]][key[1]][2]
                if ghostDistance >= -3:

                    distance = min(distance, abs(ghostDistance))

        return isGhostPresent, distance

    def replan(
        self, grid, path, ghostMap, currPathMap, currRow, currCol, nearestGhostDistance
    ):
        nextRow = path[currRow][currCol][0]
        nextCol = path[currRow][currCol][1]
        rows = [0, 0, -1, 1]
        cols = [1, -1, 0, 0]

        fRow = nextRow
        fCol = nextCol
        distanceToGhost = nearestGhostDistance
        for i in range(4):
            newRow, newCol = currRow + rows[i], currCol + cols[i]
            if (newRow, newCol == nextRow, nextCol):
                continue

            if (
                0 <= newRow < len(grid)
                and 0 <= newCol < len(grid[0])
                and grid[newRow][newCol] == 0
            ):
                pm = self.computePath(newRow, newCol, path)
                isGhostPresent, distance = self.isGhostPresentInPath(
                    ghostMap, pm, path, newRow, newCol
                )
                if isGhostPresent and distance > distanceToGhost:
                    distanceToGhost = distance
                    fRow = newRow
                    fCol = newCol
                    currPathMap = pm
                elif not isGhostPresent:
                    fRow = newRow
                    fCol = newCol
                    currPathMap = pm
                    break

        return fRow, fCol, currPathMap

    def agent2(self, currRow, currCol, grid, path, ghostMap):

        #  Computing the path after every agent step

        currPathMap = self.computePath(currRow, currCol, path)
        while True:
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                break

            isGhostPresent, distance = self.isGhostPresentInPath(
                ghostMap, currPathMap, path, currRow, currCol
            )

            if isGhostPresent:
                currRow, currCol, currPathMap = self.replan(
                    grid, path, ghostMap, currPathMap, currRow, currCol, distance
                )
                self.newGhostMap = defaultdict(int)
                for key, value in ghostMap.items():

                    g = value
                    while g > 0:
                        row = key[0]
                        col = key[1]

                        newPosition = Utility.moveGhost(row, col, grid)
                        if (currRow, currCol) == newPosition:
                            return False, grid, (currRow, currCol), ghostMap

                        self.newGhostMap[newPosition] += 1

                        g -= 1

                ghostMap = copy(self.newGhostMap)
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
                        if newAgentPosition[:2] == newPosition:
                            return False, grid, newPosition, ghostMap

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
            0, 0, grid, path, ghostMap
        )

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        print(finalAgentPosition)

        print(finalGhostPosition)

        return result


if __name__ == "__main__":
    agent2 = Agent2()

    agent2.findPath(51, 50)
