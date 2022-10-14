from collections import defaultdict
from UtilityFunctions import Utility
from MazeGeneration import MazeGeneration
from heapq import heapify, heappop
from copy import copy


class Agent4:
    def getPenalty(self, x):
        return x**2 / 5000

    def dfs(self, row, col, visited, ghostMap, path, steps):

        if steps == 5:
            return 0

        if row == len(path) - 1 and col == len(path[0]) - 1:
            return -(10**5)

        if (row, col) in ghostMap:
            # print(path[row][col])
            return (4 * ghostMap[(row, col)] * 2 * path[row][col][2]) / 10 * steps

        rows = [-1, 1, 0, 0]
        cols = [0, 0, -1, 1]

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
                    newRow,
                    newCol,
                    visited,
                    ghostMap,
                    path,
                    steps + 1,
                )
                visited.remove((newRow, newCol))
        return answer

    def agent4(self, currRow, currCol, grid, path, ghostMap, visited=defaultdict(int)):

        while True:
            visited[(currRow, currCol)] += 1
            if (currRow, currCol) in ghostMap:
                print("1")
                return False, grid, (currRow, currCol), ghostMap

            if currRow == len(grid) - 1 and currCol == len(grid[0]) - 1:
                return True, grid, (currRow, currCol), ghostMap

            # Utility.printMaze(grid)
            # print(ghostMap)

            rows = [0, 0, -1, 1]
            cols = [-1, 1, 0, 0]
            d = [
                # (
                #     self.getPenalty(visited[(currRow, currCol)]),
                #     (path[currRow][currCol][0], path[currRow][currCol][1]),
                # )
            ]

            for i in range(4):
                newRow = currRow + rows[i]
                newCol = currCol + cols[i]

                if newRow == len(grid) - 1 and newCol == len(grid[0]) - 1:
                    return True, grid, (newRow, newCol), ghostMap
                if (
                    0 <= newRow < len(grid)
                    and 0 <= newCol < len(grid[0])
                    and grid[newRow][newCol] == 0
                ):
                    d.append(
                        (
                            self.dfs(
                                newRow, newCol, {(currRow, currCol)}, ghostMap, path, 1
                            )
                            + self.getPenalty(visited[(newRow, newCol)]),
                            path[newRow][newCol][2],
                            (newRow, newCol),
                        )
                    )

            heapify(d)
            if len(d) > 0:
                direction = heappop(d)
                newAgentPosition = direction[2]
            else:
                newAgentPosition = (currRow, currCol)

            newGhostMap = defaultdict(int)
            for key, value in ghostMap.items():

                g = value
                while g > 0:
                    row = key[0]
                    col = key[1]

                    newPosition = Utility.moveGhost(row, col, grid)
                    if newAgentPosition == newPosition:
                        print("2")
                        return False, grid, newPosition, ghostMap

                    newGhostMap[newPosition] += 1

                    g -= 1

            ghostMap = copy(newGhostMap)
            # print(currRow, currCol)
            currRow = newAgentPosition[0]
            currCol = newAgentPosition[1]

    def findPath(self, gridSize, numberOfGhosts):

        self.mg = MazeGeneration()

        ghostMap = defaultdict(int)

        grid, path = self.mg.generateMaze(gridSize)

        Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

        # Utility.printMaze(grid)

        visited = defaultdict(int)

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = self.agent4(0, 0, grid, path, ghostMap, visited)

        print(result)

        # print("___________________________-")
        # Utility.printMaze(finalGrid)

        # print(finalAgentPosition)

        # print(finalGhostPosition)

        return result


if __name__ == "__main__":

    agent4 = Agent4()

    agent4.findPath(51, 5)
