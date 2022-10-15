from collections import defaultdict
from UtilityFunctions import Utility
from MazeGeneration import MazeGeneration
from heapq import heapify, heappop
from copy import copy


class Agent5:

    # This is a takeaway from Agent 3. We use the penalty
    # that grows slowly initially and grows exponentially
    # with the increase in its values so that we dont
    # visit the same cell again and again.
    def getPenalty(self, x):
        return x**2 / 5000

    # This is a DFS technique to travel round the radius
    # and check if there is a ghost in any of those cells.
    # The addition in this function is that
    # we ignore the ghosts presence if its present inside the wall.
    def dfs(self, row, col, visited, ghostMap, path, steps, grid):

        # If we reach the radius of 5, then there doesnt
        # exist any ghost and this path is more desirable in the
        # min-heap. Therefore, we return 0.
        if steps == 5:
            return 0

        # If we reach the destination, then this step is the most
        # desirable step and we return a very minimum value such that
        # this choice is at the top of the min-heap
        if row == len(path) - 1 and col == len(path[0]) - 1:
            return -(10**5)

        # If the value at the grid is odd, then it signifies a blocked cell
        # and we ignore the odd values
        if (row, col) in ghostMap and grid[row][col] % 2 != 1:
            return (4 * ghostMap[(row, col)] * 2 * path[row][col][2]) / 10 * steps

        rows = [-1, 1, 0, 0]
        cols = [0, 0, -1, 1]

        # We travel all the neighbours and
        # if the neighbour is valid, then we recursively call the function
        # upto we reach the radius of 5.
        answer = 0
        for i in range(4):
            newRow = row + rows[i]
            newCol = col + cols[i]

            if (
                0 <= newRow < len(path)
                and 0 <= newCol < len(path[0])
                and (newRow, newCol) not in visited
                and path[newRow][newCol] != -1
            ):
                visited.add((newRow, newCol))
                answer += self.dfs(
                    newRow, newCol, visited, ghostMap, path, steps + 1, grid
                )
                visited.remove((newRow, newCol))
        return answer

    def agent5(self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)):

        while True:

            # We update the number of times we visit the cell
            # in the hashmap
            visited[(currRow, currCol)] += 1

            # If there is a ghost in the current cell we are in, then
            # we return False indicating the agents death
            if (currRow, currCol) in ghostMap:
                print("1")
                return False, grid, (currRow, currCol), ghostMap

            # If the above condition fails and we reach the destination,
            # we return true
            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]
            d = [
                # (
                #     self.getPenalty(visited[(currRow, currCol)]),
                #     (path[currRow][currCol][0], path[currRow][currCol][1]),
                # )
            ]

            # Traversing the neighbours
            for i in range(4):
                newRow = currRow + rows[i]
                newCol = currCol + cols[i]

                # If the neighbour is the destination, we return True
                if newRow == len(grid) - 1 and newCol == len(grid[0]) - 1:
                    return True, grid, (newRow, newCol), ghostMap
                if (
                    0 <= newRow < len(grid)
                    and 0 <= newCol < len(grid[0])
                    and grid[newRow][newCol] == 0
                ):

                    # We append the DFS heuristic + penality + distance as our decision heuristic
                    # and the new coordinates.

                    # Our aim is to minimize this value
                    d.append(
                        (
                            self.dfs(
                                newRow,
                                newCol,
                                {(currRow, currCol)},
                                ghostMap,
                                path,
                                1,
                                grid,
                            )
                            + self.getPenalty(visited[(newRow, newCol)]),
                            path[newRow][newCol][2],
                            (newRow, newCol),
                        )
                    )

            heapify(d)

            # If the heap is empty, then staying at the same cell is taken to be a
            # desired move
            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[2]
            else:
                newAgentPosition = (currRow, currCol)

            if (newAgentPosition[0], newAgentPosition[1]) in ghostMap:
                return False, grid, (currRow, currCol), ghostMap

            newGhostMap = defaultdict(int)
            # We iterate through the ghostMap and move the ghosts
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)

                    # If we move ghost into the cell containing the agent,
                    # then we return false indicating the agents death
                    if newAgentPosition == newPosition:
                        print("2")
                        return False, grid, newPosition, ghostMap

                    newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = copy(newGhostMap)
            print(currRow, currCol)
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        Utility.printMaze(grid)

        visited = defaultdict(int)

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = self.agent5(0, 0, grid, path, ghostMap, visited)

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        # print(finalAgentPosition)

        # print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent5 = Agent5()

    agent5.findPath(51, 50)
