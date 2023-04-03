import os

import matplotlib.pyplot as plt

files = os.listdir()
result_files = []
for i in files:
    if i[0] == "(":
        result_files.append(i)

gen_result_list = []

for i in result_files:
    file = open(i, "r")
    temp = file.read().split("\n")
    temp.pop(0)
    temp.pop()
    temp = map(float, temp)
    gen_result_list.append(sum(temp))

fig = plt.figure()
gen = list(range(len(gen_result_list)))
plt.bar(gen, gen_result_list)
plt.xlabel("generation")
plt.ylabel("MSE Score")
plt.xticks(gen)
plt.savefig("overfit or underfit")
plt.show()
