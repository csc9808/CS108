"""CS 108 Final Project - Units

This module includes all the necessary classes and methods used in the Fish Tank

@author: Serita Nelesen (smn4)
@date: Fall, 2014
@author: Keith VanderLinden (kvlinden) - used particles.py and particle_simulator.py as the starting code file for this project.
@date: Fall, 2018 - updated to use callback animation
@author: Seong Chan Cho (sc77)
@date: Fall, 2020
"""
#import random to randomize choices of words and integers
from random import *

#construct a class called food
class Foods:
    '''
    this class takes in the window max width and height to draw the foods into scale
    this class acts as a parent class, it will inherit good food and bad food.
    this calss will be able to move around the canvas and have events when it collides with the fish
    '''
    def __init__(self, x= 800, y= 800,velocity = 1 ,color ='red'):  
        '''initialize/ construct Class Foods'''
        self.radius = 10
        self.x = randrange(x)
        self.y = randrange(10,y/10) 
        self.velocity = velocity
        self.color = color
        
    def render(self,canvas):
        '''this method renders/draws the food on the canvas''' 
        canvas.create_oval(
                self.x - self.radius,
                self.y - self.radius,
                self.x + self.radius,
                self.y + self.radius,
                fill=self.color
                )
        
    def move(self, canvas):
        '''this method will make the food move around the canvas'''
        self.y = (self.y + (self.velocity/4))

    def floats(self,canvas,y):
        ''' this method makes food to float in the water going up and down the canvas'''
        if (self.y <= 0 + self.radius) or (self.y >= y -self.radius ):
            self.velocity *= -1

    def hits(self, other):
        """ Determine if I've collided with 'other'. """
        if self == other:
            # I can't collide with myself.
            return False
        # Determine if I overlap with the other particle.
        return (self.radius + other.radius >=
            self.distance(self.x, self.y, other.x, other.y))
        
    def contains(self,x,y):
        '''check if one contains another'''
        if self.distance(x,y,self.x,self.y) < self.radius:
            return True
        
    def distance(self,x1, y1, x2, y2):
        """ Compute the distance between two points. """
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def set_units(self,test_x,test_y):
        ''' this method solely exists only for this file for testing as food constructor automatically randomizes the x and y value '''
        self.x = test_x
        self.y = test_y
        
# inherit from the food class. Construct a poison food class
class Poison_food(Foods):
    '''this is inherited class from the food seperated into two different class to create different interaction when fish collides with each.'''
    
    def __init__(self,x,y,velocity,color):
        '''constructor for Poison Food'''
        Foods.__init__(self,x,y,velocity,color = 'green')
        
# inherit from the food class. Construct a good food class
class Good_food(Foods):
    '''this is inherited class from the food seperated into two different class to create different interaction when fish collides with each.'''
    
    def __init__(self,x,y,velocity,color):
        '''constructor for Good Food'''
        Foods.__init__(self,x,y,velocity,color = 'brown')

#construct a Fish class
class Fish:   
    ''' this class creates a fish object in the canvas for user to freely control.'''
    
    def __init__(self,x,y,color):
        '''initialize and construct the class Fish'''
        self.x = x
        self.y = y
        self.growth = 10
        self.radius = self.growth
        self.color = color

    def render(self,canvas):
        ''' this method draws the fish on the canvas'''
        #this will create the body of the fish
        canvas.create_rectangle((self.x) - (self.growth * 4),(self.y)- (self.growth),(self.x),(self.y) + (self.growth),fill = self.color)
        #this will create the tail of the fish
        canvas.create_polygon((self.x) - (self.growth * 4),(self.y)- (self.growth),(self.x)-(self.growth * 5),(self.y)- (self.growth*2),(self.x)-(self.growth * 5),(self.y)+(self.growth*2),(self.x)-(self.growth * 4),(self.y)+(self.growth), outline = 'black',fill= self.color)
        #this will create the head of the fish
        canvas.create_oval((self.x - self.radius),(self.y-self.radius),(self.x + (self.radius)),(self.y + self.radius),fill = self.color)
        
    def move(self,canvas,x,y):
        ''' this method allows fish to start moving'''
        self.x = x
        self.y = y
        
    def grow(self,unit):
        ''' this method makes the fish grow by some unit everytime the fish eats the good food'''
        self.growth += unit
        self.radius += unit 

# exists from testing this file.
if __name__ == '__main__':
    #call for classes to see if they successfully gets called
    fish = Fish(450,450,'red')
    goodfood = Good_food(450,450,2,'brown')
    poisonfood = Poison_food(450,450,2,'green')
    #set both good and poison food with new x and y as it has been randomized when first called. 
    goodfood.set_units(450,450)
    poisonfood.set_units(450,450)
    #check if fish and foods collide with each other with hits method. 
    assert goodfood.hits(fish)
    assert poisonfood.hits(fish)
    # move to different place and then see if it doesnt collide.
    goodfood.set_units(100,100)
    poisonfood.set_units(700,700)
    assert not goodfood.hits(fish)
    assert not poisonfood.hits(fish)
    # test if fish is growing
    fish.grow(10)
    assert fish.radius > 10 



        


