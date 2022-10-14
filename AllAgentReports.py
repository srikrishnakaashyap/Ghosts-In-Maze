from Agent4 import Agent4
from Agent1 import Agent1
from Agent3 import Agent3
from Agent2 import Agent2
from Agent5 import Agent5
from Agent6 import Agent6
from statistics import mean
from MazeGeneration import MazeGeneration
from UtilityFunctions import Utility
from collections import defaultdict
from matplotlib import pyplot as plt
from MazeGeneration import *


def draw_graph(s, gh):

    plt.plot(gh, s[0], color="magenta")
    plt.plot(gh, s[1], color="black")
    plt.plot(gh, s[2], color="blue")
    plt.plot(gh, s[3], color="green")
    plt.plot(gh, s[4], color="sea")
    plt.ylabel("Success Rates (in terms of percentage)")
    plt.xlabel("Number of Ghosts")
    plt.show()


def comparison_graph():
    # Comparison Graph between Agent1, Agent2, Agent3
    pass


# def success_rate_ghost(ghosts) :
#     results = []
#     for j in range(100):
#         # further need to add the if condition for choosing the agent
#         result = agent3.findPath(51,ghosts)
#         results.append(result)

#     count = results.count(True) # returns percentage

#     return count

# def simulations(n, ghosts) :
#     avg_success = []
#     for i in range(n):
#         success = success_rate_ghost(ghosts)
#         avg_success.append(success)

#     avg = mean(avg_success)

#     return avg


def generate_report(grid, ghosts, path, ghostmap):

    ghosts_x = []
    success_y = [[], [], [], [], []]

    for i in range(ghosts, 50):
        ghosts_x.append(i)
        a = ReportAgents(grid, path, i, ghostMap)
        for j in range(5):
            success_y[j].append(a[j])

    draw_graph(success_y, ghosts_x)


def ReportAgents(grid, path, ghosts, ghostMap):

    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []

    Utility.spawnGhosts(grid, ghosts, ghostMap)

    for i in range(10):

        # result1, finalGrid1, finalAgentPosition1, finalGhostPosition1 = agent1.agent1( grid, path, ghostMap)
        # a1.append(result1)

        result2, finalGrid2, finalAgentPosition2, finalGhostPosition2 = agent2.agent2(
            0, 0, grid, path, ghostMap
        )
        a2.append(result2)

        (
            result3,
            finalGrid3,
            finalAgentPosition3,
            finalGhostPosition3,
        ) = agent3.agent3Iterative(0, 0, grid, path, ghostMap, defaultdict(int))
        a3.append(result3)

        (result4, finalGrid4, finalAgentPosition4, finalGhostPosition4) = agent4.agent4(
            0, 0, grid, path, ghostMap, defaultdict(int)
        )
        a4.append(result4)

        (result5, finalGrid5, finalAgentPosition5, finalGhostPosition5) = agent5.agent5(
            0, 0, grid, path, ghostMap, defaultdict(int)
        )
        a5.append(result5)

    a = [a1, a2, a3, a4, a5]
    print("==========================================================")
    print(a2)
    return a


if __name__ == "__main__":

    agent1 = Agent1()
    agent2 = Agent2()
    agent3 = Agent3()
    agent4 = Agent4()
    agent5 = Agent5()
    agent6 = Agent6()

    mg = MazeGeneration()

    ghostMap = defaultdict(int)

    grid, path = mg.generateMaze(51)

    ghosts = 5

    generate_report(grid, ghosts, path, ghostMap)
