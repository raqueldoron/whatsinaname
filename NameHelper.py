from tkinter import *
from genetic import generateGeneticList
from nameParser import names_parser

class Gui():
    def __init__(self):
        
        self.boy_list = names_parser(True)
        self.girl_list = names_parser(False)
        self.matrix = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.first_screen = []
        self.name_buttons = []
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

    def setBoy(self):
        for element in self.first_screen:
            element.destroy()
        self.createMatrix(True)
 
    def setGirl(self):
        for element in self.first_screen:
            element.destroy()
        self.createMatrix(False)

    def createMatrix(self, isBoy):
        explanation = Label(text = "Please choose a name you don't particurally like...", pady = 10, font = 5000, fg="black")
        explanation.grid(row=0, column=0, columnspan=6)
        nameIndex = 0;
        for y, row in enumerate(self.matrix):
            buttons_row = []
            namesList = generateGeneticList(self.boy_list) if isBoy else generateGeneticList(self.girl_list)
            for x, element in enumerate(row):
                if (isBoy):
                    nameButton = Button(self.board, text=namesList[nameIndex], fg = "blue", width=10, height=5, command=lambda a=x,b=y,name=namesList[nameIndex]: self.onButtonPressed(a,b, name, explanation, True))
                else:
                    nameButton = Button(self.board, text=namesList[nameIndex], fg = "deeppink", width=10, height=5, command=lambda a=x,b=y,name=namesList[nameIndex]: self.onButtonPressed(a,b, name, explanation, False))
                nameIndex += 1
                nameButton.grid(row=y + 1, column=x)
                buttons_row.append(nameButton)
            self.name_buttons.append(buttons_row)

    def onButtonPressed(self, x, y, namePicked, header, isBoy):
        self.name_buttons[y][x]['bg'] = 'yellow'
        header.destroy()
        for list_names in self.name_buttons:
            for name in list_names:
                name.destroy()
        self.askWhy(namePicked, isBoy)

    def askWhy(self, namePicked, isBoy):
        name_font = ("Helvetica", 30, "bold")
        name = Label(text = namePicked.capitalize(), pady=7, font = "bold")
        name.grid(row = 0, column = 0, columnspan = 6)
        name.config(font=name_font)
        name.config(fg="deepskyblue" if isBoy else "hotpink")
        self.why_buttons.append(name)
        
        why_not_font = ("verdana", 13, "bold" )
        why_not = Label(text = "Why don't you like the name?", pady=5)
        why_not.config(font = why_not_font)
        why_not.grid(row = 1, column = 0, columnspan = 6)
        self.why_buttons.append(why_not)

        semantic_reason = Button(self.board, height=5, width=10, text = "Semantic Reason", font = 50, bg = "lightgray", fg="black", padx=50)
        semantic_reason.grid(row = 2, column = 0)
        self.why_buttons.append(semantic_reason)

        syntax_reason = Button(self.board, height=5, width=10, text = "Syntax Reason", font = 50, bg = "lightgray", fg="black", padx=50)
        syntax_reason.grid(row = 2, column = 2)
        self.why_buttons.append(syntax_reason)

        personal_reason = Button(self.board, height=5, width=10, text = "Personal Reason", font = 50, bg = "lightgray", fg="black", padx=50)
        personal_reason.grid(row = 2, column = 3)
        self.why_buttons.append(personal_reason)
#         personal_reason["command"]= lambda: self.newButtons(isBoy, self.why_buttons)
#           
#           
#     def newButtons(self, isBoy, previous_screen):
#         for element in previous_screen:
#             element.destroy()
#         lambda: self.createMatrix(isBoy)



Gui().run()