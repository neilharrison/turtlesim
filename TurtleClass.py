import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageTk
import numpy as np
import math
import random

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
        self.turtle_flag = False
        self.eraser_flag = False
        self.colour_old = "black"

    def load_sprite_file(self, filename="turtle.png"):
        image = Image.open(filename)
        self.unrotatedimage = image.resize((30,int(30*image.size[0]/image.size[1])))
        self.rotatedimage = self.unrotatedimage  
    
    def load_sprite_canvas(self):
        self.loadTurtle = ImageTk.PhotoImage(self.rotatedimage)
        self.turtle_sprite = self.canvas.create_image(self.coords[0],self.coords[1],anchor=tk.CENTER, image=self.loadTurtle,tag="turtle")
        self.canvas.update()

    def rotate(self,rel_angle):
        self.canvas.delete(self.turtle_sprite)
        self.angle+=rel_angle
        self.angle = self.angle%360
        self.rotatedimage = self.unrotatedimage.rotate(self.angle)
        self.load_sprite_canvas()

    def move(self, dir, dist=10,run_over=True):
        if dir == "Up" or dir=="w":
            coord_change = np.array([0,-1])
        elif dir == "Down" or dir=="s":
            coord_change = np.array([0,1])
        elif dir == "Left" or dir=="a":
            coord_change = np.array([-1,0])
        elif dir =="Right" or dir=="d":
            coord_change = np.array([1,0])
        
        coord_change = coord_change*dist
        return self.move_to(self.coords[0]+coord_change[0],self.coords[1]+coord_change[1],run_over)

    def move_to(self,x,y,run_over=True):   
        overlaps = list(self.canvas.find_overlapping(self.coords[0], self.coords[1], x,y))

        crash = False
        overlap = False
        for i in overlaps:
            # print(self.canvas.itemconfig(i)["tags"][-1])
            if self.canvas.itemconfig(i)["tags"][-1] == "obstacle" or self.canvas.itemconfig(i)["tags"][-1] == "obstacle current":
                crash = True
        if len(overlaps)>3 and not run_over:
            overlap = True
        # print("...")     

        buffer = 5
        if not overlap and not crash and (buffer < x < self.canvas.winfo_width()-buffer) and (buffer < y < self.canvas.winfo_height()-buffer):
            if self.pen:
                self.canvas.create_line(self.coords[0], self.coords[1], x, y, fill=self.colour, width=1, tag="line")
            self.canvas.move(self.turtle_sprite,x-self.coords[0],y-self.coords[1])
            self.coords = np.array([x,y])
            self.canvas.update()
            return True
        else: return False

    def move_inc(self,x,y,run_over=True):
        num_incs = math.ceil(np.linalg.norm(np.array([x,y])-self.coords)/10)+1
        incs = np.linspace(self.coords,np.array([x,y]),num_incs)[1:]
        success = True
        for inc in incs:
            if self.move_to(inc[0],inc[1]):
                success = True 
            else: 
                success = False
                break
        return success
        
    def pen_on_off(self):
        self.pen = not self.pen

    def pick_colour(self):
        self.colour = colorchooser.askcolor(title="Pick a colour!")[1] # [1] is the hex colour

    def eraser(self):
        if self.eraser_flag:
            self.colour = self.colour_old
            self.eraser_flag = not self.eraser_flag
        else:
            self.colour_old = self.colour
            self.colour = self.canvas["background"]
            self.eraser_flag = not self.eraser_flag
    
    def reset(self):
        #slightly off centre but not a big issue
        self.coords=np.array([self.canvas.winfo_width()/2, self.canvas.winfo_height()/2])
        self.canvas.delete("all")
        self.rotate(-self.angle)
        #self.load_sprite_canvas() loaded again in rotate

    def obstacle_mouse(self,xnew,ynew):
        # Clicked outside canvas? usually when resizing window
        if self.within_range([xnew,ynew], [0,0],[self.canvas.winfo_width()-5, self.canvas.winfo_height()-20]): 
            # Check if first or second click
            if not self.obs_flag:
                if abs(self.coords[0]-xnew)<20 and abs(self.coords[1]-ynew)<20:  #clicked on turtle?
                    self.turtle_flag = True
                    print("turtle clicked")
                else:
                    self.indicator = self.canvas.create_oval(self.canvas.winfo_width()-20,20,self.canvas.winfo_width()-10,10,fill="black")
                    self.obstacle_coords = [xnew,ynew]
                self.obs_flag = True
            else: # Second click
                if self.turtle_flag:
                    tmp_pen = self.pen # keep current pen state for when finished
                    self.pen = False
                    self.move_to(xnew,ynew)
                    self.pen = tmp_pen
                    self.turtle_flag = False
                else:
                    # Check if new obstacle will enclose turtle
                    if not(self.within_range(self.coords,self.obstacle_coords,[xnew,ynew])): 
                        self.square_obstacle(self.obstacle_coords[0],self.obstacle_coords[1],xnew,ynew)
                    self.canvas.delete(self.indicator)
                self.obs_flag = False
    
    def within_range(self,check,val1,val2):
        return (val1[0]<=check[0]<=val2[0] or val2[0]<=check[0]<=val1[0]) and  (val1[1]<=check[1]<=val2[1] or val2[1]<=check[1]<=val1[1])

    def obstacle_remove(self,x,y):
        item = self.canvas.find_closest(x,y)
        if self.canvas.itemconfig(item)["tags"][-1] == "obstacle" or self.canvas.itemconfig(item)["tags"][-1] == "obstacle current":
            self.canvas.delete(item)
        self.obs_flag = False
        self.canvas.delete(self.indicator)


    def square_obstacle(self,x1,y1,x2,y2):
        self.canvas.create_rectangle(x1,y1,x2,y2,fill="black",tag="obstacle")

    
    def move_square(self,d):
        self.pen = False
        # Ugly but otherwise move is too quick, 
        self.rotate(-self.angle)
        for i in range(10):
            self.move("Up",d/20)
        self.rotate(-90)
        self.pen = True
        for i in range(10):
            self.move("Right",d/20)    
        self.rotate(-90)
        for i in range(10):
            self.move("Down",d/10)
        self.rotate(-90)
        for i in range(10):
            self.move("Left",d/10)
        self.rotate(-90)
        for i in range(10):
            self.move("Up",d/10)
        self.rotate(-90)
        for i in range(10):
            self.move("Right",d/20)
        self.rotate(-90)
        self.pen = False
        for i in range(10):
            self.move("Down",d/20)
        self.rotate(180)
        self.pen = True

    def move_circle(self,r):
        self.pen = False
        centre = self.coords
        for i in range(10):
            self.move("Up",r/10)
            
        self.rotate(-90)
        self.pen = True
        for i in range(361):
            x = centre[0]+r*math.sin(-i * math.pi/180+math.pi)
            y = centre[1]+r*math.cos(-i * math.pi/180+math.pi)
            self.move_to(x,y)
            # if i%4==0:
            #     self.canvas.update()
            if i%90==0:
                #Small rotations mess up turtle image
                self.rotate(-90)
        self.pen = False
        for i in range(10):
            self.move("Down",r/10)
        self.rotate(180)
        self.pen = True
        
    def free_space_spiral(self):
        while self.move("Up",run_over=False):
            self.canvas.update()
        while self.move("Right",run_over=False):
            self.canvas.update()
        while self.move("Down",run_over=False):
            self.canvas.update()
        while self.move("Left",run_over=False):
            self.canvas.update()
        while self.move("Up",run_over=False):
            self.canvas.update()
    
    def stuck_spiral(self, dist):
        self.move("Right",dist)
        self.canvas.update()
        self.free_space_spiral()
        self.move("Down",dist)
        self.canvas.update()
        self.free_space_spiral()
        self.move("Left",dist)
        self.canvas.update()
        self.free_space_spiral()
        self.move("Up",dist)
        self.canvas.update()
        self.free_space_spiral()

    def move_spiral(self):
        centre = self.coords
        x = centre[0]
        y = centre[1]
        j = 1
        crashed = False
        while not crashed:
            for i in range(360*(j-1),360*j):
                r = 1*i*math.pi/180
                x = centre[0]+r*math.sin(-i * math.pi/180+math.pi)
                y = centre[1]+r*math.cos(-i * math.pi/180+math.pi)
                if not self.move_to(x,y,run_over=False): 
                    crashed=True 
                    break
                if i%10==0:
                    self.canvas.update()
            j+=1
            

    def hoover_mode(self):
        # for i in range(1000):
        #     self.move_spiral()
        #     new_coords = np.array([random.randint(0,300),random.randint(0,300)])
        #     # new_coords = self.coords+np.array([random.randint(-100,100),random.randint(-100,100)])
        #     self.move_to(new_coords[0],new_coords[1])
        occupancy = np.array(np.zeros([int((self.canvas.winfo_height()-10)/10)-1, int(self.canvas.winfo_width()/10)-1]),dtype=bool)
        #occupancy maps workspace into grid of 10 pixels
        #index [0,0] => ([idx]+1)*10 => pixel (10,10)
        # while not occupancy.all():
        #do forward and backward pass in one go
        for i in range(0,occupancy.shape[0]-1,2): 
            for j in range(0,occupancy.shape[1]):
                if not occupancy[i][j]:
                    if self.move_inc((j+1)*10,(i+1)*10):
                        occupancy[i][j] = True
                    else: self.circle_obstacle(occupancy)
            for j in reversed(range(0,occupancy.shape[1])):
                if not occupancy[i+1][j]:
                    if self.move_inc((j+1)*10,(i+2)*10):
                        occupancy[i+1][j] = True
        if not occupancy.shape[0]%2==0:
            #do remaining row if odd row number
            for j in range(0,occupancy.shape[1]):
                if not occupancy[-1][j]:
                    if self.move_inc((j+1)*10,(occupancy.shape[0])*10):
                        occupancy[-1][j] = True
        
        # print("Done")
        # for i in range(30):
        #     self.stuck_spiral(i*10)
        #     self.canvas.update()
    
    def circle_obstacle(self,occupancy):
        pass

        
            
            
