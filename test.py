from tkinter import *

class Application(Frame):
    def havingBoy(self):
        print ("Woohoo! You're having a boy...")

    def havingGirl(self):
        print ("Better luck next time...You're having a girl...")
        
    def createWidgets(self):
        self.button = []
        for i in range(200):
            self.button.append(Button(self, text='Game '+str(i+1),command=lambda i=i:self.open_this(i)))
            self.button[i].grid(column=4, row=i+1, sticky=W)
#             self.button[i].pack({"side": "left"})
    def open_this(self, myNum):
        print(myNum)
        
#         self.GIRL = Button(self, height=20, width=40, text = "GIRL", font = 5000)
#         self.GIRL["fg"]   = "pink"
#         self.GIRL["command"] = self.havingGirl
# 
#         self.GIRL.pack({"side": "left"})
#         
#         self.question = Label(text = "This is to help you pick the name for your child.... are you having a boy or a girl?")
#         self.question.pack({"side": "top"})
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()