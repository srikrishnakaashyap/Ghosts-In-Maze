import random


class Utility:
    @staticmethod
    def moveGhost(row, col, grid):

        if grid[row][col] % 2 == 1:
            if random.randint(0, 1) == 0:
                return (row, col)

        rows = [0, 0, -1, 1]
        cols = [-1, 1, 0, 0]
        unblockedCells = []
        blockedCells = []
        for i in range(4):
            newRow = row + rows[i]
            newCol = col + cols[i]

            if 0 <= newRow < len(grid) and 0 <= newCol < len(grid[0]):

                if grid[newRow][newCol] % 2 == 1:
                    blockedCells.append((newRow, newCol))
                else:
                    unblockedCells.append((newRow, newCol))

        ghostMove = unblockedCells * 2 + blockedCells
        k = random.randint(0, len(ghostMove) - 1)
        grid[row][col] -= 2
        newPosition = ghostMove[k]

        nr = newPosition[0]
        nc = newPosition[1]
        # print(newPosition)
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
