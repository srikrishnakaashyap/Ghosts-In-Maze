from Agent1 import Agent1
from Agent2 import Agent2
from Agent3 import Agent3
from Agent4 import Agent4
from Agent5 import Agent5
from Agent6 import Agent6
from copy import copy, deepcopy
from MazeGeneration import MazeGeneration
from collections import defaultdict
from UtilityFunctions import Utility
import json


class ComputeAgents:
    def agent1Report(self, grid, path, ghostMap):
        agent1 = Agent1()

        result, finalGrid, finalAgentPosition, finalGhostPosition = agent1.agent1(
            grid, path, ghostMap
        )

        return result

    def agent2Report(self, grid, path, ghostMap):
        agent2 = Agent2()

        result, finalGrid, finalAgentPosition, finalGhostPosition = agent2.agent2(
            0, 0, grid, path, ghostMap
        )

        return result

    def agent3Report(self, grid, path, ghostMap):

        agent3 = Agent3()
        agent3.agent2 = Agent2()

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = agent3.agent3Iterative(0, 0, grid, path, ghostMap)

        return result

    def agent4Report(self, grid, path, ghostMap):

        agent4 = Agent4()

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = agent4.agent4(0, 0, grid, path, ghostMap)

        return result

    def agent5Report(self, grid, path, ghostMap):

        agent5 = Agent5()

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = agent5.agent5(0, 0, grid, path, ghostMap)

        return result

    def agent6Report(self, grid, path, ghostMap):

        agent6 = Agent6()

        (
            result,
            finalGrid,
            finalAgentPosition,
            finalGhostPosition,
        ) = agent6.agent6(0, 0, grid, path, ghostMap)

        return result

    def computeReport(self):

        agent1Map = {}
        agent2Map = {}
        agent3Map = {}
        agent4Map = {}
        agent5Map = {}
        agent6Map = {}


        self.mg = MazeGeneration()

        numberOfGhosts = 5
        while True:
            successRateA1 = 0
            successRateA2 = 0
            successRateA3 = 0
            successRateA4 = 0
            successRateA5 = 0
            successRateA6 = 0

            for i in range(100):
                grid, path = self.mg.generateMaze(51)
                ghostMap = defaultdict(int)
                Utility.spawnGhosts(grid, numberOfGhosts, ghostMap)

                successRateA1 += self.agent1Report(deepcopy(grid), path, deepcopy(ghostMap))
                successRateA2 += self.agent2Report(deepcopy(grid), path, deepcopy(ghostMap))
                # successRateA3 += self.agent3Report(copy(grid), path, copy(ghostMap))
                successRateA4 += self.agent4Report(deepcopy(grid), path, deepcopy(ghostMap))
                successRateA5 += self.agent5Report(deepcopy(grid), path, deepcopy(ghostMap))
                # successRateA6 += self.agent6Report(copy(grid), path, copy(ghostMap))

            agent1Map[numberOfGhosts] = successRateA1
            agent2Map[numberOfGhosts] = successRateA2
            agent3Map[numberOfGhosts] = successRateA3
            agent4Map[numberOfGhosts] = successRateA4
            agent5Map[numberOfGhosts] = successRateA5
            agent6Map[numberOfGhosts] = successRateA6

            break

        with open("agent1.json", "w") as convert_file:
            convert_file.write(json.dumps(agent1Map))

        with open("agent2.json", "w") as convert_file:
            convert_file.write(json.dumps(agent2Map))

        with open("agent3.json", "w") as convert_file:
            convert_file.write(json.dumps(agent3Map))

        with open("agent4.json", "w") as convert_file:
            convert_file.write(json.dumps(agent4Map))

        with open("agent5.json", "w") as convert_file:
            convert_file.write(json.dumps(agent5Map))

        with open("agent6.json", "w") as convert_file:
            convert_file.write(json.dumps(agent6Map))

        return True


if __name__ == "__main__":
    cp = ComputeAgents()

    cp.computeReport()
