from tkinter import END

import pygame
import tkinter as tk
import tkinter.font as tkFont

import Game
import Learning.Learning

if __name__ == '__main__':
    pygame.init()
    displayModes = pygame.display.list_modes()

    root = tk.Tk()
    root.title("Display Selection")
    root.geometry('20x10')
    root.resizable(False,False)

    textFont = tkFont.Font(family='Times', size=10)

    displayListBox = tk.Listbox(root)

    scrollbar = tk.Scrollbar(root)

    displayListBox.configure(justify="center", font=textFont, selectmode="single", setgrid=True,yscrollcommand=scrollbar.set)
    displayListBox.grid(row=0,column=1,sticky=tk.NS)

    scrollbar.configure(command=displayListBox.yview)

    for i in displayModes:displayListBox.insert(END,i)

    resolutionText = tk.Message(root)
    resolutionText.configure(font=textFont, text="Resolution")
    resolutionText.grid(row=0,column=0)

    def StartLearning():
        index = displayListBox.curselection()
        x_display_dim = displayListBox.get(index)[0]
        y_display_dim = displayListBox.get(index)[1]
        root.destroy()
        Learning.Learning.LearningScreen(x_display_dim, y_display_dim)


    def StartGame():
        index = displayListBox.curselection()
        x_display_dim = displayListBox.get(index)[0]
        y_display_dim = displayListBox.get(index)[1]
        root.destroy()
        Game.GameScreen(x_display_dim,y_display_dim)

    buttonGame = tk.Button(root)
    buttonGame.configure(font=textFont, justify="center",text="Start Game", command=StartGame)
    buttonGame.grid(row=1,column=0)

    buttonLearn = tk.Button(root)
    buttonLearn.configure(font=textFont, justify="center", text="Start Learn", command=StartLearning)
    buttonLearn.grid(row=1,column=2)

    root.mainloop()

