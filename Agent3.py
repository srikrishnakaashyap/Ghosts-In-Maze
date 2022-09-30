from MazeGeneration import MazeGeneration
import random
from collections import deque
from UtilityFunctions import Utility
from collections import defaultdict
from copy import copy


class Agent3:
    def recursiveDFS(self, grid, visited, ghostMap, currRow, currCol, path):

        if path[-1] == (len(grid) - 1, len(grid[0]) - 1):
            self.allPaths.append(path[:])
            return

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]

        self.newGhostMap = defaultdict(int)
        for key, value in ghostMap.items():

            g = value
            while g > 0:
                # print(g)
                row = key[0]
                col = key[1]

                newPosition = Utility.moveGhost(row, col, grid)
                if path[-1] == newPosition:
                    return
                self.newGhostMap[newPosition] += 1

                g -= 1

        ghostMap = copy(self.newGhostMap)

        for j in range(4):
            newRow = currRow + rows[j]
            newCol = currCol + cols[j]

            if (
                0 <= newRow < len(grid)
                and 0 <= newCol < len(grid[0])
                and ghostMap[(newRow, newCol)] == 0
                and grid[newRow][newCol] == 0
                and (newRow, newCol) not in visited
            ):
                # moved = True
                visited.add((newRow, newCol))
                path.append((newRow, newCol))
                self.recursiveDFS(grid, visited, ghostMap, newRow, newCol, path)
                path.pop(-1)
                visited.remove((newRow, newCol))

        return

    def findPath(self, numberOfGhosts):
        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid = self.mg.generateMaze(5)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        Utility.printMaze(grid)

        print(ghostMap)

        path = [(0, 0)]

        self.allpaths = []

        visited = set()
        visited.add((0, 0))

        self.recursiveDFS(grid, visited, ghostMap, 0, 0, path)

        print("FINAL MAZEE")
        print("-----------------------------")
        Utility.printMaze(grid)

        print(self.newGhostMap)
        # print("-----------------------------")

        # print(self.allpaths)
        # print(path)


if __name__ == "__main__":

    agent3 = Agent3()

    agent3.findPath(3)
