"""CS 108 Final Project - GUI

This module implements a GUI controller for Fish Tank

@author: Serita Nelesen (smn4)
@date: Fall, 2014
@author: Keith VanderLinden (kvlinden) - used particles.py and particle_simulator.py as the starting code file for this project.
@date: Fall, 2018 - updated to use callback animation
@author: Seong Chan Cho (sc77)
@date: Fall, 2020
"""
# import necessary modules
from tkinter import *
from Units import *
import random

#create class called App
class App:
    def __init__(self, window):
        """Instantiate the simulation GUI window."""
        self.window = window
        #set background image
        self.image = PhotoImage(file="fishtank.png")
        self.width = self.image.width()
        self.height = self.image.height()
        self.rate = 5
        self.current_score = IntVar()
        self.current_score.set(0)
        self.scorelabel = StringVar()
        self.scorelabel.set('Welcome, Please Enter your name!')
        self.greeting_message = StringVar()
        self.greeting_message.set('')
        self.user = ''
        # Give two different colors to foods, one real food and on poisonous food.
        self.color = random.choice(['brown','green'])
        #Back ground 
        #learnt how to make cursor invisible from -> (https://stackoverflow.com/questions/20446782/how-to-hide-or-disable-the-mouse-pointer-in-tkinter)  
        self.canvas = Canvas(window, width=self.width, height=self.height,cursor = 'none')
        self.canvas.create_image(0, 0, anchor=NW, image=self.image)
        self.canvas.pack()
        #make a label for text messages including scores and directions
        self.scoretext = Label(self.window, textvariable = self.scorelabel)
        self.scoretext.pack()
        #create a score label for integer score
        self.score = Label(self.window,textvariable = self.current_score,width = 10, height= 5)
        self.score.pack()
        #create an entry for user to type name
        self.name = StringVar()
        self.user_name = Entry(window,  font="arial 16",textvariable=self.name)
        self.user_name.pack(side=LEFT)
        self.user_name.focus_set()
        self.user_name.bind("<Return>", self.get_name)
        #create a restart Button
        self.restart_button = Button(self.window, text="Restart",command= self.restart)
        self.restart_button.pack()
        #empty list for foods showing in water(background)
        self.good_food_list = []
        self.poison_food_list = []
        #create a fish class
        self.fish = Fish(self.width,self.height,'orange')
        #Enable mouse interaction on screen
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<Button-1>', self.add_food)
        #Start Animation
        self.running = True
        self.window.after(0,self.animation)
        
    def animation(self):
        ''' this method loops the main animation that happens in the GUI'''
        if self.running == True:
            self.canvas.delete(ALL)
            # image idea derived from the image.py from project samples
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)
            self.fish.render(self.canvas)
            # create good food and show what effects it has when collided.
            for gf in self.good_food_list:
                gf.render(self.canvas)
                gf.move(self.canvas)
                gf.floats(self.canvas,self.height)
                if gf.hits(self.fish):
                    self.good_food_list.remove(gf)
                    self.current_score.set(self.current_score.get() + 10)
                    self.fish.grow(0.3)
            # create poisoned food and show what effects it has when collided.
            for pf in self.poison_food_list:
                pf.render(self.canvas)
                pf.move(self.canvas)
                pf.floats(self.canvas,self.height)
                if pf.hits(self.fish):
                    self.poison_food_list.remove(pf)
                    self.running = False
                    # this try and except will give different outputs to different results from the game
                    try:
                        with open('scoreboard.txt','r') as f:
                            highscore = f.read()
                            # result when user beats highscore
                            if self.current_score.get() > int(highscore):
                                with open('scoreboard.txt','w') as file:
                                    file.write(str(self.current_score.get()))
                                    self.scorelabel.set(self.user.get() + ', Congratulation!\nYou have achieved a new highscore. \nYour Final Score is :')
                            #result when user gets the same score as the highscore in the leader
                            elif self.current_score.get() == int(highscore):
                                self.scorelabel.set(self.user.get() + '...One more food and you could have been the champion... \nYour Final Score is :')
                            #result when user gets lower score than the highest score
                            else:
                                self.scorelabel.set(self.user.get() + '... You died... You could not beat the highest score!\nThe highest score in the leaderboard is: ' + highscore + '\nYour Final Score is :')
                    # Deny user to record his/her score as they did not enter their name.
                    except:
                        self.scorelabel.set('You have not entered any name before the game, Your score will not be recorded!')
        self.window.after(self.rate, self.animation)
    
    def add_food(self,event):     
        ''' this method allows user to click on the screen to feed the fish'''
        count = 0
        food_choice = [1,2]
        #create a while loop so the food gets created N number of times. 
        while count < 4:
            create_food = random.choice(food_choice)
            # set a if / else statement so that everytime it loops it randomly either creates the good food or the poison food. 
            if create_food == 1:
                new_good_food= Good_food(self.width,self.height,randrange(1,10),'brown')
                self.good_food_list.append(new_good_food)
            else:
                new_poison_food= Poison_food(self.width,self.height,randrange(1,10),'green')
                self.poison_food_list.append(new_poison_food)
            count +=1

    def motion(self,event):
        ''' this method allows user to control the fish with mouse'''
        self.fish.move(self.canvas,event.x,event.y)
        
    def restart(self):
        ''' this method will allow user to restart the game'''
        self.poison_food_list.clear()
        self.good_food_list.clear()
        self.current_score.set(0)
        self.user =''
        self.name.set('')
        self.scorelabel.set('Welcome! Please re-enter your name\nScore: ')
        self.fish = Fish(self.width,self.height,'orange')
        self.running = True
        
    def get_name(self,event):
        '''this method gets user name only when game is running. It exists to deny users to deny them from entering their names when game is stopped'''
        if self.running == True:
            self.user = self.name
            self.scorelabel.set(self.user.get() + '\n Score: ')

            
# Initialize the Game
if __name__ == '__main__':
    root = Tk()
    root.title('My Dear Fish!')    
    app = App(root)
    root.mainloop()
