import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk
import numpy as np

class Turtle:
    
    def __init__(self, canvas): 
        self.canvas = canvas
        self.coords = np.array([150, 150])
        self.load_sprite_file()
        self.load_sprite_canvas()
        self.pen = True
        self.colour = '#000000'
        self.angle = 0
        self.obs_flag = False

    def load_sprite_file(self, filename="turtle.png"):
        image = Image.open(filename)
        self.resizeimage = image.resize((30,int(30*image.size[0]/image.size[1])))
    
    def load_sprite_canvas(self):
        self.loadTurtle = ImageTk.PhotoImage(self.resizeimage)
        self.turtle_sprite = self.canvas.create_image(self.coords[0]-15,self.coords[1]-self.resizeimage.size[1]/2,anchor=tk.NW, image=self.loadTurtle,tag="turtle")
    
    def rotate(self,angle):
        self.canvas.delete(self.turtle_sprite)
        self.resizeimage = self.resizeimage.rotate(angle)
        self.angle+=angle
        self.load_sprite_canvas()

    def move(self, dir, dist=10):
        if dir == "Up" or dir=="w":
            coord_change = np.array([0,-1])
        elif dir == "Down" or dir=="s":
            coord_change = np.array([0,1])
        elif dir == "Left" or dir=="a":
            coord_change = np.array([-1,0])
        elif dir =="Right" or dir=="d":
            coord_change = np.array([1,0])
        
        coord_change = coord_change*dist

        overlaps = list(self.canvas.find_overlapping(self.coords[0], self.coords[1], self.coords[0]+coord_change[0],self.coords[1]+coord_change[1]))
        crash = False
        for i in overlaps:
            if self.canvas.itemconfig(i)["tags"][-1] == "obstacle" or self.canvas.itemconfig(i)["tags"][-1] == "obstacle current":
                crash = True
                
        buffer = 2
        if not crash and (buffer < self.coords[0]+coord_change[0] < self.canvas.winfo_width()-buffer) and (buffer < self.coords[1]+coord_change[1] < self.canvas.winfo_height()-buffer):
            if self.pen:
                self.canvas.create_line(self.coords[0], self.coords[1], self.coords[0]+coord_change[0], self.coords[1]+coord_change[1], fill=self.colour, width=1, tag="line")
            self.canvas.move(self.turtle_sprite,coord_change[0],coord_change[1])
            self.coords += coord_change

    def reset(self):
        #slightly off centre but not a big issue
        self.coords=np.array([self.canvas.winfo_width()/2, self.canvas.winfo_height()/2])
        self.canvas.delete("all")
        self.rotate(-self.angle)
        #self.load_sprite_canvas() loaded again in rotate

    def obstacle_mouse(self,xnew,ynew):
        if not self.obs_flag:
            self.obstacle_coords = [xnew,ynew]
            self.obs_flag = True
        else:
            self.square_obstacle(self.obstacle_coords[0],self.obstacle_coords[1],xnew,ynew)
            self.obs_flag = False
    
    def obstacle_remove(self,x,y):
        item = self.canvas.find_closest(x,y)
        if self.canvas.itemconfig(item)["tags"][-1] == "obstacle" or self.canvas.itemconfig(item)["tags"][-1] == "obstacle current":
            self.canvas.delete(item)
        self.obs_flag = False


    def square_obstacle(self,x1,y1,x2,y2):
        self.canvas.create_rectangle(x1,y1,x2,y2,fill="black",tag="obstacle")

    def pen_on_off(self):
        self.pen = not self.pen

    def pick_colour(self):
        self.colour = colorchooser.askcolor(title="Pick a colour!")[1] # [1] is the hex colour