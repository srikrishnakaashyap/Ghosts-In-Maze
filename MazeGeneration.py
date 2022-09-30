import random
from collections import deque

"""
0 -> Unblocked
1 -> wall
2 -> ghost in unblocked
3 -> ghost in blocked


To spawn a ghost, increment it by 2
to remove a ghost, decrement it by 2
"""


class MazeGeneration:
    def fillBlockedArray(self, blockedNumbers):

        ctr = 0

        while ctr < 28:
            n = random.randint(0, 99)
            if blockedNumbers[n] == 0:
                blockedNumbers[n] = 1
                ctr += 1

    def checkMaze(self, grid):
        queue = deque()

        path = [[-1 for i in range(len(grid[0]))] for j in range(len(grid))]

        queue.append((len(grid) - 1, len(grid[0]) - 1))
        visited = set()

        visited.add((len(grid) - 1, len(grid[0]) - 1))

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]
        while queue:
            n = len(queue)
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
                        visited.add((newRow, newCol))
                        queue.append((newRow, newCol))
                        path[newRow][newCol] = (element[0], element[1])

        if path[0][0] == -1:
            return False, []

        path[-1][-1] = 100
        return True, path

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

    grid = mg.generateMaze(51)

    # mg.printMaze(grid)
    print("COUNT OF BLOCKED = ", mg.getCount(grid))
