import os
import pickle

import sys

from Learning.model import Agent

sys.path.insert(0, os.path.abspath("../"))

import Food


class EA:
    def __init__(self, folder):

        self.folder = folder

        # extract information from the files
        WINNER_FILE = folder + "/winners.txt"

        f = open(WINNER_FILE, "r")
        self.winners_list = f.read().split("\n")

        while "" in self.winners_list:
            self.winners_list.remove("")

    def evaluate(self, agent):
        none_winner = "A-Star Static"

        # the x is a list with list in float (need to make it to list with float (individualism))
        score = 0
        for index, win in enumerate(self.winners_list):
            if win == "None":
                pickle_file = self.folder + "/Steps/" + none_winner + "/" + str(index) + ".pickle"
            else:
                pickle_file = self.folder + "/Steps/" + win + "/" + str(index) + ".pickle"
            file_data = open(pickle_file, 'rb')

            extracted_data = pickle.load(file_data)

            food_location = extracted_data.pop()
            agent.body = extracted_data[0][0]

            food = Food.Food(agent.body)
            food.foodX = food_location[0]
            food.foodY = food_location[1]

            state, steps = agent.tunningWeights(agent, food)

            winner_step_num = len(extracted_data)

            # if the agent manage to solve an impossible game
            if win == "None" and state:
                score += 30
            elif win == "None" and not state:
                pass
            elif win == "Random Search" and not state:
                pass
            elif win == "Random Search" and state:
                # might need to consider this reward (might be training to a garbage model (further thinking needed, or possible evaluation material))
                score += 20
            elif state:
                score += (10 - (len(steps) - winner_step_num))
            else:
                # this is for if the winner data is not random search or no victor and didn't manage to get to a victor
                score -= winner_step_num

        return score


def main(folder, agent):
    score = []

    directories = os.listdir(folder)

    for i in directories:
        final_folder = folder + "/" + i

        ea = EA(final_folder)

        score.append(ea.evaluate(agent))

    print(score)


if __name__ == '__main__':
    file = open("../Learning/result.txt", "r")

    text = file.read().split("\n")

    temp = text[-3].split("is ")[1]
    temp = temp.split(" at")[0]
    values = temp.split(",")
    final_values = []
    for i in values:
        final_values.append(float(i))

    agent = Agent(final_values)

    FOLDER = "../data"
    main(FOLDER, agent)
