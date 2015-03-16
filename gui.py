from tkinter import *
from PIL import ImageTk
from time import sleep
from random import choice as choose_from_seq
from collections.abc import ItemsView

class GUI(Frame):
    def __init__(self, master, computerAgent, databaseHandler):
        Frame.__init__(self, master)
        self.master = master
        self.agent = computerAgent
        self.dbhandler = databaseHandler
        
        self.user_action = None
        self.computer_action = None
        self.records = []
        self.stats = {'com':0, 'user':0, 'games':0}
        
        
        self.silenceButtons = False # boolean needed for writing the records without "RSP" buttons jumping as choices
        
        # Canvas - the place all the pictures gets drawn
        self.canvas = Canvas(master, width=400, height=200, bg = "white")
        self.canvas.grid(row=0,column=0, columnspan=2)
        self.canvas_pictures = dict() # here will be stored all the pictures
       
        # the scores
        self.score_user_sv = StringVar()
        self.score_computer_sv = StringVar()
        Label(master, textvariable = self.score_user_sv).grid(row = 1, column = 0)
        Label(master, textvariable = self.score_computer_sv, justify = RIGHT).grid(row = 1, column = 1)
        self.score_user_sv.set("you: 0")
        self.score_computer_sv.set("super-agent: 0")
        

       
        
        # bind keyboard key presses to the events
        self.master.bind('<Key>',
                              self.key_pressed)

        # tell the computer the first game has begun
        self.getComputerAgentAction()
        
        
        if self.silenceButtons:
            return
        key = str(event.char).lower()
        try:
            function = GUI.keys_to_functions[key] # this is a dictionary storing the functions for rellevant keys
            function(self, key)
        except KeyError: # a key without a function - just pass
            pass

    def user_made_a_choice(self, choice): # choice is a char
        if not self.user_action:         # only record one try
            self.user_action = choice
            #self.string_gui.set("") # clear the entry
            #drawing
            picturePath = GUI.path_for_images["decision"]
            self.user_picture = PhotoImage(file = picturePath)
            # save the picture so we can erase it later
            temp = self.canvas.create_image(100,100, image = self.user_picture)
            self.canvas_pictures["user_decision"] = temp
            
            self.start_game() # start_game() checks if both computer and human have made their choice
            
    
    def computer_made_a_choice(self, choice = None):
        ''' the computer choice. if not given any - will choose randomly '''
        if not choice: # or choice == 'd':
            choice = choose_from_seq("rsp") # randomly choosing among the options
        self.computer_action = choice

        # drawing
        picturePath = GUI.path_for_images["decision"]
        self.computer_picture = PhotoImage(file = picturePath)
        # save the picture
        temp = self.canvas.create_image(300,100, image=self.computer_picture)
        self.canvas_pictures["computer_decision"] = temp

        self.start_game() # start_game() checks if both computer and human have made their choice

    def start_game(self):
        if not (self.computer_action and self.user_action):
            return

        
        TIME_TO_WAIT = 1000
        NEW_COMPUTER_CHOICE = 2500
        THRD_LAP = False
                    
        # calculate the winner
        winner = self.checkWinner() #'c' for computer_winning , 'h' for human_winning, 't' for tie
        if winner == 'c':
            self.stats['com'] += 1
        elif winner == 'h':
            self.stats['user'] += 1
        self.stats['games'] += 1
        record = (self.computer_action, self.user_action, winner)
        self.records.append(record)
        if not (self.stats['games'] % 3): # third game
            THRD_LAP = True
            l3r = self.records[-3:] # last 3 records
            self.dbhandler.update_game(l3r[0], l3r[1], l3r[2]) # update last 3 games
            NEW_COMPUTER_CHOICE += 3000 # wait three seconds before next game
        self.after(TIME_TO_WAIT, self.draw_lap, self.user_action, self.computer_action, THRD_LAP)
        self.computer_action = self.user_action = None


        # inform the computer about a new game -
        self.after(NEW_COMPUTER_CHOICE, self.getComputerAgentAction)
           
    def getComputerAgentAction(self):
        act = self.agent.getAction()
        self.computer_made_a_choice(act)
        
    def checkWinner(self):
        ''' called only by start_game() after making sure there is no user mis-input '''
        if self.user_action == self.computer_action:
            return 't' # for TIE
        elif    (self.user_action == 'r' and self.computer_action == 's') \
            or  (self.user_action == 's' and self.computer_action == 'p') \
            or  (self.user_action == 'p' and self.computer_action == 'r'):    
            return 'h' # for HUMAN
        else:
            return 'c' # for COMPUTER
            
    def draw_lap(self, u, c, third_lap):
        ''' given the user and the computer actions, draw them on the canvas '''
        TIME_TO_WAIT = 1000
        
        # erase the former pictures
        user_picture = self.canvas_pictures["user_decision"]
        computer_picture = self.canvas_pictures["computer_decision"]
        self.canvas.delete(user_picture)
        self.canvas.delete(computer_picture)
        # create new ones -
        # user
        picturePath = GUI.path_for_images[u]
        self.user_picture = PhotoImage(file = picturePath)
        user_picture = self.canvas.create_image(100,100, image=self.user_picture)
        # computer
        picturePath = GUI.path_for_images[c]
        self.computer_picture = PhotoImage(file = picturePath)
        computer_picture = self.canvas.create_image(300,100, image=self.computer_picture)
        
        # update the counters at the bottom of the screen
        self.score_computer_sv.set("super-agent: "+str(self.stats['com'])) 
        self.score_user_sv.set("you: "+str(self.stats['user']))
        #  clear all variables and pictures for the next round
        self.after(TIME_TO_WAIT, self.clear_canvas, (user_picture, computer_picture))
        
        if third_lap:
            self.after(TIME_TO_WAIT, self.draw_new_game)
        '''
        self.canvas.delete(user_picture)
        self.canvas.delete(computer_picture)
        '''
        
    def clear_canvas(self, items_to_delete = []):
        ''' clear the canvas '''
        if not items_to_delete:
            self.canvas.delete(ALL)
        else:
            for i in items_to_delete:
                self.canvas.delete(i)
            
    def draw_new_game(self):
        picturePath = GUI.path_for_images["3rd_lap"]
        self.img = PhotoImage(file = picturePath)
        actual_pic = self.canvas.create_image(200,100, image=self.img)
        self.after(2000, self.clear_canvas, [actual_pic])
        
        
    def display_all_and_exit(self, key = None):
        self.player_name = StringVar()
        self.player_name.set("What is your name? (Required for the prize that is way better than chocolate)")
        Label(self.master, textvariable = self.player_name).grid(row = 4, column = 0, columnspan = 2)
        self.entryForName = Entry(self.master)
        self.entryForName.grid(row=5, column=0, columnspan = 2)
        Button(self.master, text='Quit', command=self.exit).grid(row=6, column=0, columnspan = 2)

        # silence the 'RSP' buttons
        self.silenceButtons = True
        

    def exit(self):
        ''' updating the DB and exiting '''
        USER_POINTS = 30
        playerName = knowledge = self.entryForName.get()
        if self.stats['com'] <= self.stats['user'] and self.stats['user'] >= USER_POINTS:
            knowledge += "_chocolate_ok"
        self.stats = {'com':0, 'user':0, 'games':0}
        if playerName:
            print(playerName + ", ", end = '')
        print("Thanks for your Help! We really aprriciate it :) \n")
        self.dbhandler.update_db_end_of_game(knowledge)
        self.master.quit()

    keys_to_functions = {'r':user_made_a_choice,
                         'p':user_made_a_choice,
                         's':user_made_a_choice,
                         'q':display_all_and_exit #,
#                         'd':computer_made_a_choice
                        }
    path_for_images = {'s':"/cs/stud/masha_eowyn/rsp/pic/scissors.gif",
                       'r':"/cs/stud/masha_eowyn/rsp/pic/rock.gif",
                       'p':"/cs/stud/masha_eowyn/rsp/pic/paper.gif",
                       "decision":"/cs/stud/masha_eowyn/rsp/pic/choice.gif",
                       "3rd_lap":"/cs/stud/masha_eowyn/rsp/pic/3rd_lap.gif"
                       }
