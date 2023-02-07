import pickle
import random

from deap import creator, base, tools

import Food
from Learning import model

# extract information from the files
FILE_DIR = "F:/test/05_02_2023 17_55_57/"
WINNER_FILE = FILE_DIR + "winners.txt"

f = open(WINNER_FILE, "r")
winners_list = f.read().split("\n")

while "" in winners_list:
    winners_list.remove("")

class EA():
    def __init__(self):
        IND_SIZE = 6
        FIXED_RANGE_VALUE = 15

        creator.create("FitnessMax", base.Fitness, weights=(2.0, 1.0, 2.0, 1.0, 2.0, 1.0))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # this part is the framework to create new instances (individual or a whole pop (random))
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, -FIXED_RANGE_VALUE, FIXED_RANGE_VALUE)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, n=IND_SIZE)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.population = self.toolbox.population(10)

        def evaluate(x):
            none_winner = "A-Star"

            # the x is a list with list in float (need to make it to list with float (individualism))
            agent = model.Agent(x)
            score = 0
            for index, win in enumerate(winners_list):
                if win == "None":
                    pickle_file = FILE_DIR + "/Steps/" + none_winner + "/" + str(index) + ".pickle"
                else:
                    pickle_file = FILE_DIR + "/Steps/" + win + "/" + str(index) + ".pickle"
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

                print(index)

            return score

        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("evaluate", evaluate)

    # generate new population and have some mutation on it (sigma and indpb should be a hyperparam (take note))
    def repopulate(self, selected):
        self.population = selected
        for i in range(len(selected)):
            mutant = self.toolbox.clone(selected[i])
            ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)

            del mutant.fitness.values

            self.population.append(ind2)
        return self.population


if __name__ == '__main__':

    # create the stuff
    ea = EA()

    # possible fix here for the error (use the toolsbox)
    fitness = list(map(ea.toolbox.evaluate, ea.population))
    for ind, fit in zip(ea.population, fitness):
        ind.fitness.values = fit
    test = [ind.fitness.values[0] for ind in ea.population]
    print(test)
