import matplotlib.pyplot as plt
import numpy
import numpy as np

AccAlgo = open("Evaluation/Score/AccumAlgo.txt", "r")

acc_result_list = AccAlgo.read().split("\n")
acc_result_list.pop()

acc_round_nums = []
acc_resets = []
acc_food_gained = []

# acc_round_nums_std = []
# acc_resets_std = []
# acc_food_gained_std = []
#
# acc_round_nums_avg = []
# acc_resets_avg = []
# acc_food_gained_avg = []

for v in acc_result_list:
    i = v.split(", ")
    acc_round_nums.append(int(i[0]))
    acc_resets.append(int(i[1]))
    acc_food_gained.append(int(i[2]))

# acc_round_nums_avg = sum(acc_round_nums) / len(acc_round_nums)
# acc_round_nums_std = numpy.std(acc_round_nums)
#
# acc_resets_avg = sum(acc_resets) / len(acc_resets)
# acc_resets_std = numpy.std(acc_resets)
#
# acc_food_gained_avg = sum(acc_food_gained) / len(acc_food_gained)
# acc_food_gained_std = numpy.std(acc_food_gained)

Model = open("Evaluation/Score/Model.txt", "r")

model_result_list = Model.read().split("\n")
model_result_list.pop()

model_round_nums = []
model_resets = []
model_food_gained = []

# model_round_nums_std = []
# model_resets_std = []
# model_food_gained_std = []
#
# model_round_nums_avg = []
# model_resets_avg = []
# model_food_gained_avg = []

for d in model_result_list:
    i = d.split(", ")
    model_round_nums.append(int(i[0]))
    model_resets.append(int(i[1]))
    model_food_gained.append(int(i[2]))

# model_round_nums_avg = sum(model_round_nums) / len(model_round_nums)
# model_round_nums_std = numpy.std(model_round_nums)
#
# model_resets_avg = sum(model_resets) / len(model_resets)
# model_resets_std = numpy.std(model_resets)
#
# model_food_gained_avg = sum(model_food_gained) / len(model_food_gained)
# model_food_gained_std = numpy.std(model_food_gained)

# Creating axes instance
# ax = fig.add_axes([0, 0, 1, 1])

round_nums = [np.array(model_round_nums), np.array(acc_round_nums)]
reset_nums = [np.array(model_resets), np.array(acc_resets)]
food_gained_nums = [np.array(model_food_gained), np.array(acc_food_gained)]

# Creating plot
plt.boxplot(round_nums)
plt.title("rounds per test")
plt.xticks([1, 2], ["Model", "Acc Algo"])

# show plot
plt.show()

plt.boxplot(reset_nums)
plt.title("number of resets (100 tests)")
plt.xticks([1, 2], ["Model", "Acc Algo"])

# show plot
plt.show()

plt.boxplot(food_gained_nums)
plt.title("number of food gained (100 tests)")
plt.xticks([1, 2], ["Model", "Acc Algo"])

# show plot
plt.show()
