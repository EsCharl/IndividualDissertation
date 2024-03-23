import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind

def t_test(set0, set1):
    return ttest_ind(set0, set1)

def graphing(model_test_round_nums, model_test_resets, model_test_food_gained):

    round_nums = [np.array(model_round_nums), np.array(acc_round_nums)]
    reset_nums = [np.array(model_resets), np.array(acc_resets)]
    food_gained_nums = [np.array(model_food_gained), np.array(acc_food_gained)]
    ratio_final = [np.array(model_food_gained) / np.array(model_resets),
                   np.array(acc_food_gained) / np.array(acc_resets)]

    round_nums.append(np.array(model_test_round_nums))
    reset_nums.append(np.array(model_test_resets))
    food_gained_nums.append(np.array(model_test_food_gained))

    # Creating plot
    plt.boxplot(round_nums)
    plt.title("rounds per test (higher the better)")
    plt.xticks([1, 2, 3], ["Model", "Acc Algo", "Model (gen move first)"])

    # show plot
    plt.show()

    plt.boxplot(reset_nums)
    plt.title("number of resets (100 tests), (lower the better)")
    plt.xticks([1, 2, 3], ["Model", "Acc Algo", "Model (gen move first)"])

    # show plot
    plt.show()

    plt.boxplot(food_gained_nums)
    plt.title("number of food gained (100 tests), (higher the better)")
    plt.xticks([1, 2, 3], ["Model", "Acc Algo", "Model (gen move first)"])

    # show plot
    plt.show()
    
    ratio_final.append(np.array(model_test_food_gained) / np.array(model_test_resets))
    plt.boxplot(ratio_final)
    plt.title("ratio between food gained and reset (higher the better)")
    plt.xticks([1, 2, 3], ["Model", "Acc Algo", "Model (gen move first)"])

    # show plot
    plt.show()

if __name__ == '__main__':
    AccAlgo = open("Evaluation/Score/AccumAlgo.txt", "r")

    acc_result_list = AccAlgo.read().split("\n")
    acc_result_list.pop()

    acc_round_nums = []
    acc_resets = []
    acc_food_gained = []

    for v in acc_result_list:
        i = v.split(", ")
        acc_round_nums.append(int(i[0]))
        acc_resets.append(int(i[1]))
        acc_food_gained.append(int(i[2]))

    Model = open("Evaluation/Score/Model.txt", "r")

    model_result_list = Model.read().split("\n")
    model_result_list.pop()

    model_round_nums = []
    model_resets = []
    model_food_gained = []

    for d in model_result_list:
        i = d.split(", ")
        model_round_nums.append(int(i[0]))
        model_resets.append(int(i[1]))
        model_food_gained.append(int(i[2]))

    round_nums = [np.array(model_round_nums), np.array(acc_round_nums)]
    reset_nums = [np.array(model_resets), np.array(acc_resets)]
    food_gained_nums = [np.array(model_food_gained), np.array(acc_food_gained)]

    Model_test = open("Evaluation/Score/model gen moves first.txt", "r")

    model_test_result_list = Model_test.read().split("\n")
    model_test_result_list.pop()

    model_test_round_nums = []
    model_test_resets = []
    model_test_food_gained = []

    for d in model_test_result_list:
        i = d.split(", ")
        model_test_round_nums.append(int(i[0]))
        model_test_resets.append(int(i[1]))
        model_test_food_gained.append(int(i[2]))

    graphing(model_test_round_nums, model_test_resets, model_test_food_gained)

    print(t_test(np.array(model_food_gained) / np.array(model_resets), np.array(model_test_food_gained) / np.array(model_test_resets)))

    print(t_test(np.array(model_food_gained) / np.array(model_resets), np.array(acc_food_gained) / np.array(acc_resets)))

    print(t_test(np.array(model_test_food_gained) / np.array(model_test_resets), np.array(acc_food_gained) / np.array(acc_resets)))

