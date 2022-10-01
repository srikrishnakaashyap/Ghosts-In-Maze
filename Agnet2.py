from MazeGeneration import MazeGeneration
from collections import defaultdict


class Agent2:
    def computePath(self, row, col, path):

        pathArray = []

        while True:
            if row == len(path) - 1 and col == len(path[0]) - 1:
                break
            pathArray.append((row, col))

            newPos = path[row][col]
            row = newPos[0]
            col = newPos[1]

        return pathArray

    def agent2(self, grid, path, ghostMap):

        #  Computing the path after every agent step

        currPathArray = self.computePath(p)

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)


if __name__ == "__main__":
    agent2 = Agent2()

    agent2.findPath(5, 1)
