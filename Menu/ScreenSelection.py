import os.path
import sys
from tkinter import END

import pygame
import tkinter as tk
import tkinter.font as tkFont

sys.path.insert(0, os.path.abspath("../"))

import Game
import Learning.GeneratingData


def main():
    pygame.init()
    displayModes = pygame.display.list_modes()

    root = tk.Tk()
    root.title("Display Selection")
    root.resizable(False, False)

    textFont = tkFont.Font(family='Times', size=10)

    displayListBox = tk.Listbox(root)

    scrollbar = tk.Scrollbar(root)

    displayListBox.configure(justify="center", font=textFont, selectmode="single", setgrid=True,
                             yscrollcommand=scrollbar.set)
    displayListBox.grid(row=0, column=1, sticky=tk.NS)

    scrollbar.configure(command=displayListBox.yview)

    # reason why 1.6 is selected is because it looks better and the borders are viewable
    for i in displayModes:
        if i[0] / i[1] == 1.6:
            displayListBox.insert(END, i)

    resolutionText = tk.Message(root)
    resolutionText.configure(font=textFont, text="Resolution")
    resolutionText.grid(row=0, column=0)

    def LearningOption():
        index = displayListBox.curselection()
        x_display_dim = displayListBox.get(index)[0]
        y_display_dim = displayListBox.get(index)[1]
        root.destroy()

        options = tk.Tk()
        options.title("Learning Options")

        number_data = tk.Spinbox(options, from_=500, to=100000, textvariable=tk.StringVar(value="1000"))
        number_data.grid(row=0, column=2, sticky=tk.NS)

        number_data_text = tk.Message(options)
        number_data_text.configure(font=textFont, text="num data gen")
        number_data_text.grid(row=0, column=0)

        number_population = tk.Spinbox(options, from_=150, to=450, textvariable=tk.StringVar(value="300"))
        number_population.grid(row=1, column=2, sticky=tk.NS)

        number_population_text = tk.Message(options)
        number_population_text.configure(font=textFont, text="Pop in each gen")
        number_population_text.grid(row=1, column=0)

        generation = tk.Spinbox(options, from_=5, to=50, textvariable=tk.StringVar(value="10"))
        generation.grid(row=2, column=2, sticky=tk.NS)

        generation_text = tk.Message(options)
        generation_text.configure(font=textFont, text="total gen")
        generation_text.grid(row=2, column=0)

        cross_over_prob = tk.Spinbox(options, from_=0.1, to=1.0, increment=0.05, textvariable=tk.StringVar(value="0.5"))
        cross_over_prob.grid(row=4, column=2, sticky=tk.NS)

        cross_over_prob_text = tk.Message(options)
        cross_over_prob_text.configure(font=textFont, text="Cross over prob")
        cross_over_prob_text.grid(row=4, column=0)

        mutation_prob = tk.Spinbox(options, from_=0.1, to=1.0, increment=0.05, textvariable=tk.StringVar(value="0.2"))
        mutation_prob.grid(row=6, column=2, sticky=tk.NS)

        mutation_prob_text = tk.Message(options)
        mutation_prob_text.configure(font=textFont, text="Mutation prob")
        mutation_prob_text.grid(row=6, column=0)

        first_range_value = tk.Spinbox(options, from_=-100, to=100.0, textvariable=tk.StringVar(value="-15"))
        first_range_value.grid(row=8, column=2, sticky=tk.NS)

        first_range_value_text = tk.Message(options)
        first_range_value_text.configure(font=textFont, text="first range value")
        first_range_value_text.grid(row=8, column=0)

        second_range_value = tk.Spinbox(options, from_=-100, to=100.0, textvariable=tk.StringVar(value="15"))
        second_range_value.grid(row=10, column=2, sticky=tk.NS)

        second_range_value_text = tk.Message(options)
        second_range_value_text.configure(font=textFont, text="second range value")
        second_range_value_text.grid(row=10, column=0)

        startLearningButton = tk.Button(options)
        startLearningButton.grid(row=12, column=1, sticky=tk.NS)

        def ActivateLearning():
            data = int(number_data.get())
            pop = int(number_population.get())
            gen = int(generation.get())
            cross = float(cross_over_prob.get())
            mutation = float(mutation_prob.get())
            first_val = int(first_range_value.get())
            second_val = int(second_range_value.get())

            options.quit()
            options.destroy()
            Learning.GeneratingData.LearningScreen(data, pop, gen, cross, mutation, first_val, second_val,
                                                   x_display_dim, y_display_dim)

        startLearningButton.configure(font=textFont, justify="center", text="Learn Game",
                                      command=ActivateLearning)

        options.mainloop()

    def GameOption():
        index = displayListBox.curselection()
        x_display_dim = displayListBox.get(index)[0]
        y_display_dim = displayListBox.get(index)[1]
        root.destroy()

        options = tk.Tk()
        options.title("Game Options")

        time_text = tk.Message(options)
        time_text.configure(font=textFont, text="game time")
        time_text.grid(row=0, column=0)

        time = (3, 5, 10)

        timeListBox = tk.Listbox(options)
        for t in time: timeListBox.insert(END, t)

        timeListBox.configure(selectmode="single")
        timeListBox.grid(row=0, column=2)

        startGameButton = tk.Button(options)
        startGameButton.configure(font=textFont, justify="center", text="Start Game", command=lambda: options.quit())
        startGameButton.grid(row=1, column=1, columnspan=2)

        options.mainloop()

        timeAmount = timeListBox.get(timeListBox.curselection())
        options.destroy()

        Game.GameScreen(x_display_dim, y_display_dim, timeAmount)

    buttonGame = tk.Button(root)
    buttonGame.configure(font=textFont, justify="center", text="Game", command=GameOption)
    buttonGame.grid(row=1, column=0)

    buttonLearn = tk.Button(root)
    buttonLearn.configure(font=textFont, justify="center", text="Learn", command=LearningOption)
    buttonLearn.grid(row=1, column=2)

    root.mainloop()


if __name__ == '__main__':
    main()
