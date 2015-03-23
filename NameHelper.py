from tkinter import *
from genetic import generateGeneticList
from nameParser import names_parser

class Gui():
    def __init__(self):
        malesSorted = open("malesSorted.txt", "r")
        femalesSorted = open("femalesSorted.txt", "r")
        malesSorted = malesSorted.read()
        femalesSorted = femalesSorted.read()
        self.boy_list = malesSorted.split("\n")
        self.girl_list = femalesSorted.split("\n")
        self.matrix = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.first_screen = []
        self.second_screen = []
        self.why_buttons = []
        self.board = Tk()
        self.board.title('What\'s in a Name?')
        self.firstScreen()

    def run(self):
        self.board.mainloop()
    
    def firstScreen(self):
        question_font = ("verdana", 12, "bold")
        question = Label(text = "Boy or Girl?", padx=17.5)
        question.config(font = question_font)
        question.grid(row = 0, column = 1)
        self.first_screen.append(question)
        
        boy_girl_font = ("verdana", 18)
        GIRL = Button(self.board, height=5, width=15, text = "Girl", activebackground = "pink", activeforeground = "white")
        GIRL.config(font = boy_girl_font)
        GIRL["fg"] = "deeppink"
        GIRL["command"] = self.setGirl
        GIRL.grid(row = 0, column = 2)
        self.first_screen.append(GIRL)

        BOY = Button(self.board, height=5, width=15, text = "Boy", activebackground = "lightblue", activeforeground = "white")
        BOY.config(font = boy_girl_font)
        BOY["fg"]   = "blue"
        BOY["command"] = self.setBoy
        BOY.grid(row = 0, column = 0)
        self.first_screen.append(BOY)
    def removeScreen(self, screen_elements):
        for element in screen_elements:
            element.destroy()

    def setBoy(self):
        self.removeScreen(self.first_screen)
        self.create_names_table("semantics", True)
 
    def setGirl(self):
        self.removeScreen(self.first_screen)
        self.create_names_table("semantics", False)
    
    def create_names_table(self, group, isBoy):
        dislikes = []
        if group == "semantics":
            message = "Names you like for SEMANTICS reasons (meaning, origin, tradition etc.):"
        else:
            message = "Names you like for SYNTAX reasons (sound, length, letter etc.):"
        explanation = Label(text = message, pady = 10, font = 5000, fg="black")
        self.second_screen.append(explanation)
        explanation.grid(row=0, column=0, columnspan=6)
        doneButton = Button(self.board, text="DONE", fg="black", font="bold", activebackground="red", width=70, command =lambda list=dislikes: self.onDonePressed(group, list, isBoy))
        self.second_screen.append(doneButton)
        doneButton.grid(row=1, column=0, columnspan=6)
        nameIndex = 0;
        for y, row in enumerate(self.matrix):
            buttons_row = []
            namesList = generateGeneticList(self.boy_list) if isBoy else generateGeneticList(self.girl_list)
            for x, element in enumerate(row):
                nameButton = Checkbutton(self.board, text=namesList[nameIndex], fg = "blue" if isBoy else "deeppink", width=10, height=5, command=lambda a=x,b=y,name=namesList[nameIndex]: self.onButtonPressed(a,b, name, dislikes))
                nameIndex += 1
                nameButton.grid(row=y + 2, column=x)
                self.second_screen.append(nameButton)

    
    def onButtonPressed(self, x, y, namePicked, bad_names_list):  
        place = y*6 + x + 2
        if self.second_screen[place]['bg'] == 'yellow':
            bad_names_list.remove(namePicked)
            self.second_screen[place]['bg'] = "#edeceb"
        else:
            bad_names_list.append(namePicked)
            self.second_screen[place]['bg'] = 'yellow'
        print(bad_names_list)
        
    def onDonePressed(self, group, bad_names_list, isBoy):
        self.removeScreen(self.second_screen)
        self.showNames(bad_names_list, isBoy)
    
    def showNames(self, bad_names_list, isBoy):
        
        didnt_like_font = ("verdana", 15, "bold" )
        didnt_like = Label(text = "Names you like for semantic reasons:", pady=5)
        didnt_like.config(font = didnt_like_font)
        didnt_like.grid(row = 0, column = 0, columnspan = 6)
        self.why_buttons.append(didnt_like)


        name_font = ("Helvetica", 12, "bold")
        name = Label(text = bad_names_list, pady=7, font = "bold")
        name.grid(row = 1, column = 0, columnspan = 6)
        name.config(font=name_font)
        name.config(fg="deepskyblue" if isBoy else "hotpink")
        self.why_buttons.append(name)


Gui().run()