from tkinter import END

import pygame
import tkinter as tk
import tkinter.font as tkFont

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

        frame = tk.Frame(options)
        frame.pack()

        startLearningButton = tk.Button(frame)
        startLearningButton.configure(font=textFont, justify="center", text="Learn Game",
                                      command=lambda: options.quit())
        startLearningButton.pack(side="bottom")

        options.mainloop()

        options.destroy()

        Learning.LearningComponent.LearningScreen(x_display_dim, y_display_dim)

    def GameOption():
        index = displayListBox.curselection()
        x_display_dim = displayListBox.get(index)[0]
        y_display_dim = displayListBox.get(index)[1]
        root.destroy()

        options = tk.Tk()
        options.title("Game Options")
        options.geometry("200x250")

        frame = tk.Frame(options)
        frame.pack()

        time = (3, 5, 10)

        timeListBox = tk.Listbox(frame)
        for t in time: timeListBox.insert(END, t)

        timeListBox.configure(selectmode="single")
        timeListBox.pack(side="top")

        startGameButton = tk.Button(frame)
        startGameButton.configure(font=textFont, justify="center", text="Start Game", command=lambda: options.quit())
        startGameButton.pack(side="bottom")

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
