import math
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
        total_score = 0
        score_list = []
        for index, win in enumerate(self.winners_list):
            predicted_score = 0
            actual_score = 0
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

            # used to get the total expected score
            if not win == "None":
                total_score += 10
                actual_score = 10

            if state:
                predicted_score = (10 - (len(steps) - winner_step_num))
                score += predicted_score
            elif not state and not win == "None":
                # this is for if the winner data is not random search or no victor and didn't manage to get to a victor
                score -= winner_step_num
                predicted_score -= winner_step_num

            score_list.append(math.pow(actual_score - predicted_score, 2))

        return [score, total_score, score_list]


def main(folder, agent):
    score = []

    directories = os.listdir(folder)

    for i in directories:
        final_folder = folder + "/" + i

        ea = EA(final_folder)

        score.append(ea.evaluate(agent))

    return score


if __name__ == '__main__':
    file = open("../Learning/result.txt", "r")

    text = file.read().split("\n")
    text.pop()

    ind = 0

    for i in list(range(len(text))):
        if i % 2 == 0:
            temp = text[i].split("is ")[1]
            temp = temp.split(" at")[0]
            values = temp.split(",")
            final_values = []
            for i in values:
                final_values.append(float(i))

            agent = Agent(final_values)

            FOLDER = "../data"
            val = main(FOLDER, agent)

            file = open("(" + str(ind) + ") "+", ".join(list(map(str, final_values))) + ".txt", "w")
            file.write(str(val) + "\n")

            ind += 1

            for y in val:
                file.write(str(sum(y[2]) / len(y[2])) + "\n")

            file.close()
