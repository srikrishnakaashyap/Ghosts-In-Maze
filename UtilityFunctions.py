import random


class Utility:
    @staticmethod
    def moveGhost(row, col, grid):

        if grid[row][col] % 2 == 1:
            if random.randint(0, 1) == 0:
                return (row, col)

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]

        ghostMove = []

        for i in range(4):
            newRow = row + rows[i]
            newCol = col + cols[i]

            if 0 <= newRow < len(grid) and 0 <= newCol < len(grid[0]):

                ghostMove.append((newRow, newCol))
        k = random.randint(0, len(ghostMove) - 1)
        newPosition = ghostMove[k]

        nr = newPosition[0]
        nc = newPosition[1]

        if grid[nr][nc] % 2 == 1:
            m = random.randint(0, 1)
            if m == 0:
                return (row, col)
        grid[row][col] -= 2
        grid[nr][nc] += 2
        return newPosition

    @staticmethod
    def spawnGhosts(grid, numberOfGhosts, ghostMap):
        number = 0

        while number < numberOfGhosts:
            randomRow = random.randint(0, len(grid) - 1)
            randomCol = random.randint(0, len(grid[0]) - 1)

            # print(randomRow, randomCol)

            if (randomRow == 0 and randomCol == 0) or (
                randomRow == len(grid) - 1 and randomCol == len(grid[0]) - 1
            ):
                continue

            grid[randomRow][randomCol] += 2
            ghostMap[(randomRow, randomCol)] += 1
            number += 1

    @staticmethod
    def printMaze(grid):

        for row in grid:
            print(row)
