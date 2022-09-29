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
        grid[newPosition[0]][newPosition[1]] += 2
        return newPosition

    @staticmethod
    def spawnGhosts(grid, numberOfGhosts, ghostSet):
        number = 0

        while number < numberOfGhosts:
            randomRow = random.randint(0, len(grid) - 1)
            randomCol = random.randint(0, len(grid[0]) - 1)

            print(randomRow, randomCol)

            if (randomRow, randomCol) in ghostSet:
                continue

            grid[randomRow][randomCol] += 2
            ghostSet.add((randomRow, randomCol))
            number += 1

        # Utility.printMaze(grid)
        # return grid, ghostSet

    @staticmethod
    def printMaze(grid):

        for row in grid:
            print(row)
