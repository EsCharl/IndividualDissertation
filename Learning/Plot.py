import numpy
import matplotlib.pyplot as plt


class Plotting:
    def __init__(self):
        self.y = []

    def recordPlot(self, y):
        self.y.append(y)
        
    def finalisePlot(self):
        x = list(range(len(self.y)))

        std = []
        avg = []
        for i in self.y:
            std.append(numpy.std(i))
            avg.append(sum(i) / len(i))

        fig, ax = plt.subplots()
        ax.errorbar(x, avg, yerr=std, capsize=3, capthick=3)
        ax.set_xlabel("generation")
        ax.set_ylabel("score")
        plt.xlim(-1)
        plt.xticks(numpy.arange(0, len(self.y) + 1, step=1))
