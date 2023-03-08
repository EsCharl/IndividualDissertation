import os
import pickle
import random

from deap import creator, base, tools

import sys

sys.path.insert(0, os.path.abspath("../"))

import Food
from Learning import model, Plot


class EA:
    def __init__(self, folder, pop_size):
        TOUR_SIZE = pop_size / 2

        # extract information from the files
        WINNER_FILE = folder + "/winners.txt"

        f = open(WINNER_FILE, "r")
        winners_list = f.read().split("\n")

        while "" in winners_list:
            winners_list.remove("")

        IND_SIZE = 6
        FIXED_RANGE_VALUE = 15
        POPULATION_SIZE = 300

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # this part is the framework to create new instances (individual or a whole pop (random))
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, -FIXED_RANGE_VALUE, FIXED_RANGE_VALUE)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, n=IND_SIZE)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.population = self.toolbox.population(POPULATION_SIZE)

        def evaluate(x):
            none_winner = "A-Star Static"

            # the x is a list with list in float (need to make it to list with float (individualism))
            agent = model.Agent(x)
            score = 0
            for index, win in enumerate(winners_list):
                if win == "None":
                    pickle_file = folder + "/Steps/" + none_winner + "/" + str(index) + ".pickle"
                else:
                    pickle_file = folder + "/Steps/" + win + "/" + str(index) + ".pickle"
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

            return score,

        # sigma and indpb should be a hyperparam (take note)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        self.toolbox.register("select", tools.selTournament, tournsize=TOUR_SIZE)
        self.toolbox.register("evaluate", evaluate)


def main(folder, pop_size=300, generation_limit=10, cross_over_prob=0.5, mutation_prob=0.2):
    # random.seed(1)

    # create the stuff
    ea = EA(folder, pop_size)

    plotting_component = Plot.Plotting()

    fitness = list(map(ea.toolbox.evaluate, ea.population))

    print(fitness)
    print(type(fitness))

    for ind, fit in zip(ea.population, fitness):
        ind.fitness.values = fit

    scores = [ind.fitness.values[0] for ind in ea.population]
    print(scores)

    best_ind = tools.selBest(ea.population, 1)[0]

    print(type(best_ind), type(best_ind.fitness.values))
    print(type(str(best_ind)), type(str(best_ind.fitness.values)))
    print(best_ind, best_ind.fitness.values)
    f = open("data.txt", "w")
    f.write("Best individual is %s at %s" % (",".join(map(str, best_ind)),
                                             str(best_ind.fitness.values[0])) + '\n' +
            ", ".join(map(str, scores)) + "\n")
    f.close()

    print("Best individual is %s at %s" % (",".join(map(str, best_ind)),
                                           str(best_ind.fitness.values[0])) + '\n' +
          ", ".join(map(str, scores)) + "\n")

    plotting_component.ConPlot(scores)

    for i in range(generation_limit - 1):
        offspring = ea.toolbox.select(ea.population, len(ea.population))

        offspring = list(map(ea.toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cross_over_prob:
                ea.toolbox.mate(child1, child2)

                del child1.fitness.values
                del child2.fitness.values

        for child in offspring:
            if random.random() < mutation_prob:
                ea.toolbox.mutate(child)
                del child.fitness.values

        # this part is used to get all the missing scores based on the mutation and crossovers
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        fitness = list(map(ea.toolbox.evaluate, invalid_ind))

        for ind, fit in zip(invalid_ind, fitness):
            ind.fitness.values = fit

        ea.population[:] = offspring

        # this part is just to see the score of all individual (deletable)
        scores = [ind.fitness.values[0] for ind in ea.population]
        print(scores)

        # this part is just for aesthetic (deletable)
        best_ind = tools.selBest(ea.population, 1)[0]

        f = open("data.txt", "a")
        f.write("Best individual is %s at %s" % (",".join(map(str, best_ind)),
                                                 str(best_ind.fitness.values[0])) + '\n' +
                ", ".join(map(str, scores)) + "\n")
        f.close()

        print("Best individual is %s at %s" % (",".join(map(str, best_ind)),
                                               str(best_ind.fitness.values[0])) + '\n' +
              ", ".join(map(str, scores)) + "\n")

        # show plot
        plotting_component.ConPlot(scores)


if __name__ == '__main__':
    FOLDER = "../data/03_03_2023 21_45_23"
    main(FOLDER)
