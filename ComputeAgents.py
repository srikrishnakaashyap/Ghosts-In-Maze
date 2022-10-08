from Agent1 import Agent1
from Agent2 import Agent2
from Agent3 import Agent3
import json


class ComputeAgents:
    def agent1Report(self, agent1Map):
        numberOfGhosts = 5

        while True:
            successRate = 0

            for i in range(100):
                successRate += Agent1().findPath(51, numberOfGhosts)

            if successRate > 0:
                agent1Map[numberOfGhosts] = successRate
                print(
                    "Agent 1 Success Rate is {} for {} ghosts".format(
                        successRate, numberOfGhosts
                    )
                )
                numberOfGhosts += 1
            else:
                return

    def agent2Report(self, agent2Map):
        numberOfGhosts = 5

        while True:
            successRate = 0

            for i in range(100):
                successRate += Agent1().findPath(51, numberOfGhosts)

            if successRate > 0:
                agent2Map[numberOfGhosts] = successRate
                print(
                    "Agent 2 Success Rate is {} for {} ghosts".format(
                        successRate, numberOfGhosts
                    )
                )
                numberOfGhosts += 1
            else:
                return

    def agent3Report(self, agent3Map):
        numberOfGhosts = 5

        while True:
            successRate = 0

            for i in range(100):
                successRate += Agent3().findPath(51, numberOfGhosts)

            if successRate > 0:
                agent3Map[numberOfGhosts] = successRate
                print(
                    "Agent 3 Success Rate is {} for {} ghosts".format(
                        successRate, numberOfGhosts
                    )
                )
                numberOfGhosts += 1
            else:
                return

    def computeReport(self):

        agent1Map = {}
        agent2Map = {}
        agent3Map = {}

        self.agent1Report(agent1Map)
        with open("agent1.json", "w") as convert_file:
            convert_file.write(json.dumps(agent1Map))

        self.agent2Report(agent2Map)
        with open("agent2.json", "w") as convert_file:
            convert_file.write(json.dumps(agent2Map))

        self.agent3Report(agent3Map)

        # convert_file.close

        with open("agent3.json", "w") as convert_file:
            convert_file.write(json.dumps(agent3Map))

        print("AGENT 1", agent1Map)
        print("AGENT 2", agent2Map)
        print("AGENT 3", agent3Map)

        return True


if __name__ == "__main__":
    cp = ComputeAgents()
