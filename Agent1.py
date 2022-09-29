from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility


class Agent1:
    def recursiveDFS(self, grid, visited, ghostSet, currRow, currCol, path):

        if path[-1] == (len(grid) - 1, len(grid[0]) - 1):
            return path

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]

        newGhostSet = set()

        for element in ghostSet:
            row = element[0]
            col = element[1]

            newPosition = Utility.moveGhost(row, col, grid)
            if path[-1] == newPosition:
                return -1
            newGhostSet.add(newPosition)

        ghostSet = newGhostSet

        for j in range(4):
            newRow = currRow + rows[j]
            newCol = currCol + cols[j]

            if (
                0 <= newRow < len(grid)
                and 0 <= newCol < len(grid[0])
                and (newRow, newCol) not in ghostSet
                and grid[newRow][newCol] == 0
            ):
                # moved = True
                visited.add((newRow, newCol))

                path.append((newRow, newCol))
                self.recursiveDFS(grid, visited, ghostSet, newRow, newCol, path)
                path.pop(-1)
                visited.remove((newRow, newCol))
        return []

    def findPath(self, numberOfGhosts):
        self.mg = MazeGeneration()

        ghostSet = set()

        grid = self.mg.generateMaze(10)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostSet)

        print("GHOST SET", ghostSet)

        Utility.printMaze(grid)

        path = [(0, 0)]

        visited = set()

        # self.recursiveDFS(grid, visited, ghostSet, 0, 0, path)

        # Utility.printMaze(grid)

        # print(path)


if __name__ == "__main__":

    agent1 = Agent1()

    agent1.findPath(5)
