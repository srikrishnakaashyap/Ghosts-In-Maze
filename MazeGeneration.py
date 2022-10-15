import random
from collections import deque
from UtilityFunctions import Utility

"""
0 -> Unblocked
1 -> wall
2 -> ghost in unblocked
3 -> ghost in blocked


To spawn a ghost, increment it by 2
to remove a ghost, decrement it by 2
"""

# This class is used to generate a maze and return the maze
# along with the precomputed path that contains the next cell the agent
# needs to move to reach the goal along with the
# distance to destination.
class MazeGeneration:

    # This function is used to randomly select 28 indices in an array of size 100,
    # and make the values in those cells 1.
    # This array is further used on each cell. A random number between 0 and 100 is generated
    # and the value of this array in that index is copied into the grid.
    def fillBlockedArray(self, blockedNumbers):

        ctr = 0

        while ctr < 28:
            n = random.randint(0, 99)
            if blockedNumbers[n] == 0:
                blockedNumbers[n] = 1
                ctr += 1

    # This function runs a BFS algorithm starting the destination node till the source node.
    # If we are able to reach the source, then we consider the maze to be valid.
    def checkMaze(self, grid):
        queue = deque()

        # This is the datastructure we will be using to store the next cell
        # that needs to be visited along with the distance to the destination.
        path = [[-1 for i in range(len(grid[0]))] for j in range(len(grid))]

        queue.append((len(grid) - 1, len(grid[0]) - 1, 0))
        visited = set()

        visited.add((len(grid) - 1, len(grid[0]) - 1))

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]
        while queue:
            n = len(queue)

            # This loop is used to traverse the grid
            # in a level order fashion
            for i in range(n):
                element = queue.popleft()

                for i in range(4):
                    newRow = element[0] + rows[i]
                    newCol = element[1] + cols[i]

                    if (
                        0 <= newRow < len(grid)
                        and 0 <= newCol < len(grid[0])
                        and (newRow, newCol) not in visited
                        and grid[newRow][newCol] != 1
                    ):

                        # We add the visited cell to the set so that we dont visit it again.
                        visited.add((newRow, newCol))
                        queue.append((newRow, newCol, element[2] + 1))

                        # Here, we update the parent from which we have visited the new row.
                        # When we update these values for all the cells in the maze, we finally have the distance
                        # stored along with the next cell that it needs to visit.
                        path[newRow][newCol] = (element[0], element[1], element[2] + 1)

        # if the source cell wasn't reached,
        # then the maze is invalid.
        if path[0][0] == -1:
            return False, []

        # If the source cell is reached, we use 100 to be a place holder value.
        # Note: This value hasn't been used in this project and has no significance.
        path[-1][-1] = 100
        return True, path

    # Given a value of n, this function generates a maze of size n * n
    # and returns the grid and the precomputed path if the grid is valid.
    # If the maze is invalid, then the same function is called recursively,
    # until it returns a valid maze.
    def generateMaze(self, n):
        grid = [[0 for i in range(n)] for j in range(n)]

        blockedNumbers = [0 for i in range(100)]
        self.fillBlockedArray(blockedNumbers)

        for i in range(n):
            for j in range(n):
                if (i == 0 and j == 0) or (i == n - 1 and j == n - 1):
                    continue

                index = random.randint(0, 99)
                grid[i][j] = blockedNumbers[index]

        result, path = self.checkMaze(grid)

        if result:
            return grid, path
        return self.generateMaze(n)

    def getCount(self, grid):
        answer = 0

        for row in grid:
            answer += row.count(1)

        return answer


if __name__ == "__main__":

    mg = MazeGeneration()

    grid, path = mg.generateMaze(10)

    # Utility.printMaze(grid)

    # print("_________________________")
    # Utility.printMaze(path)

    for row in grid:
        for col in row:
            print(col, "& ", end="")
        print()

    for row in path:
        for col in row:
            print(col, "& ", end="")
        print()

    # mg.printMaze(grid)
    # print("COUNT OF BLOCKED = ", mg.getCount(grid))
