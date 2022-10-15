from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
from copy import deepcopy


class Agent2:

    # Given the current row and the current column
    # and the path array, this function computes a path
    # and returns the planned path in a hashmap.
    # We used the hashmap to have a constant access time to check
    # if a ghost is in the planned path in O(1) time.
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

    # This function is used to check if a ghost is present in the
    # computed path or not. If the ghost is present, then this function
    # returns the distance of the closest ghost in the path in terms of
    # the number of steps.
    def isGhostPresentInPath(self, ghostMap, currPathMap, path, currRow, currCol):
        distance = len(currPathMap)
        isGhostPresent = False

        # We iterate through every ghost location and check
        # if the ghost is present in our path.
        for key, value in ghostMap.items():

            if key in currPathMap:
                isGhostPresent = True
                ghostDistance = path[currRow][currCol][2] - path[key[0]][key[1]][2]
                if ghostDistance >= -3:

                    # If the ghost is present, we update the distance
                    # to the closest ghost
                    distance = min(distance, abs(ghostDistance))

        return isGhostPresent, distance

    # Given the current state of the ghost and the distance of the
    # closest ghost and current agents position,
    # this function takes a detour and returns the next step.
    def replan(
        self, grid, path, ghostMap, currPathMap, currRow, currCol, nearestGhostDistance
    ):

        # This is the next cell that it should have visited in the absence of
        # the ghost.
        nextRow = path[currRow][currCol][0]
        nextCol = path[currRow][currCol][1]
        rows = [0, 0, -1, 1]
        cols = [1, -1, 0, 0]

        fRow = nextRow
        fCol = nextCol
        distanceToGhost = nearestGhostDistance

        # We iterate through all the adjacent cells
        for i in range(4):
            newRow, newCol = currRow + rows[i], currCol + cols[i]
            if (newRow, newCol == nextRow, nextCol):
                continue

            if (
                0 <= newRow < len(grid)
                and 0 <= newCol < len(grid[0])
                and grid[newRow][newCol] == 0
            ):
                # If the adjacent cell is valid, we compute a new path from the
                # adjacent cell and find the distance of the closest ghost.
                pm = self.computePath(newRow, newCol, path)
                isGhostPresent, distance = self.isGhostPresentInPath(
                    ghostMap, pm, path, newRow, newCol
                )

                # If the ghost is not present in the path,
                # then we break out and choose the path. But if the ghost is present,
                # then we check if the distance of the closest ghost is further than our original
                # distance. If yes, then we update our path.
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

        # finally, we return the updated position along with
        # the path map.
        return fRow, fCol, currPathMap

    def agent2(self, currRow, currCol, grid, path, ghostMap):

        #  Computing the path after every agent step

        # We compute the path map that stores the planned path
        currPathMap = self.computePath(currRow, currCol, path)
        while True:

            # If there is a ghost in the current cell we are in, then
            # we return False indicating the agents death
            if (currRow, currCol) in ghostMap:
                print("1")
                return False, grid, (currRow, currCol), ghostMap

            # If the above condition fails and we reach the destination,
            # we break out of the loop.
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                break

            # We check if the ghost is present in our planned path
            isGhostPresent, distance = self.isGhostPresentInPath(
                ghostMap, currPathMap, path, currRow, currCol
            )

            # If the ghost is present, we replan to a new cell and since
            # the agent moved, we move all the ghosts in the maze.
            # If the ghost isnt present, then we move in the planned path and move
            # the ghosts by iterating the ghostMap.
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

                        # If we move ghost into the cell containing the agent,
                        # then we return false indicating the agents death
                        if (currRow, currCol) == newPosition:
                            return False, grid, (currRow, currCol), ghostMap

                        self.newGhostMap[newPosition] += 1

                        g -= 1

                ghostMap = deepcopy(self.newGhostMap)
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

                ghostMap = deepcopy(self.newGhostMap)

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
