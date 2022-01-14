import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk
import numpy as np

class Turtle:
    
    def __init__(self, canvas): 
        self.canvas = canvas
        self.coords = np.array([150, 150])
        self.load_sprite()
        self.pen = True
        self.colour = '#000000'

    def load_sprite(self, filename="turtle.png"):
        image = Image.open(filename)
        resizeimage = image.resize((30,int(30*image.size[0]/image.size[1])))
        self.loadTurtle = ImageTk.PhotoImage(resizeimage)
        self.turtle_sprite = self.canvas.create_image(self.coords[0]-15,self.coords[1]-resizeimage.size[1]/2,anchor=tk.NW, image=self.loadTurtle)
    
    def move(self, dir, dist=10):
        if dir == "Up":
            coord_change = np.array([0,-1])
        elif dir == "Down":
            coord_change = np.array([0,1])
        elif dir == "Left":
            coord_change = np.array([-1,0])
        elif dir =="Right":
            coord_change = np.array([1,0])

        coord_change = coord_change*dist

        if self.pen:
            self.canvas.create_line(self.coords[0], self.coords[1], self.coords[0]+coord_change[0], self.coords[1]+coord_change[1], fill=self.colour, width=1)
        self.canvas.move(self.turtle_sprite,coord_change[0],coord_change[1])
        self.coords += coord_change


    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def pen_on_off(self):
        self.pen = not self.pen

    def pick_colour(self):
        self.colour = colorchooser.askcolor(title="Pick a colour!")[1] # [1] is the hex colour