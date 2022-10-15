import random

# This is a utility class consisting of static methods
# to perform the basic and common operations on the maze.
class Utility:

    # Given the current position row, col of the ghost,
    # this function is used to move the ghost to the next cell.
    # This function is called for every ghost in the maze.
    @staticmethod
    def moveGhost(row, col, grid):

        # If the value at the grid is an odd value, then this signifies
        # that the current cell is valid.
        # Hence, we generate a random number between 0 and 1 and if it is 0,
        # then we stay at the same cell.
        # We have assumed that the probability of randomly selecting 0 is 50%.
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

        # Append all the possible steps a ghost can take into an array
        # and choosing a random index in the array.
        k = random.randint(0, len(ghostMove) - 1)
        newPosition = ghostMove[k]

        nr = newPosition[0]
        nc = newPosition[1]

        # If the randomly selected cell is blocked, then similar to the above
        # idea, we generate a random number between 0 and 1 and take an appropriate decision.
        if grid[nr][nc] % 2 == 1:
            m = random.randint(0, 1)
            if m == 0:
                return (row, col)

        # Decrementing the value at the old index by 2 and increment the value at the new index
        # by 2. This updates the maze and returns the new position
        grid[row][col] -= 2
        grid[nr][nc] += 2
        return newPosition

    # Given grid, the number of ghosts and a hashmap to store
    # the locations of the ghosts, this function spawns the ghost in the grid
    # and updates its location in the hashmap.
    # By spawning the ghost, we mean that the value at the particular cell is incremented by 2
    # along with updating the location in the ghost map.
    @staticmethod
    def spawnGhosts(grid, numberOfGhosts, ghostMap):
        number = 0

        while number < numberOfGhosts:

            # Randomly selecting a row number and column number within the bounds
            randomRow = random.randint(0, len(grid) - 1)
            randomCol = random.randint(0, len(grid[0]) - 1)

            # print(randomRow, randomCol)

            # We have avoided spawning the ghost at the source cell
            # and the destination cell initially. However, we have not restricted
            # the movement of the ghost to reach either of these cells in any way.
            if (randomRow == 0 and randomCol == 0) or (
                randomRow == len(grid) - 1 and randomCol == len(grid[0]) - 1
            ):
                continue

            # Since our maze supports having multiple ghosts at the same cell,
            # we have simply incremented the value at the cell by 2.
            grid[randomRow][randomCol] += 2
            ghostMap[(randomRow, randomCol)] += 1
            number += 1

    # This function is used to print the maze
    @staticmethod
    def printMaze(grid):

        for row in grid:
            print(row)
