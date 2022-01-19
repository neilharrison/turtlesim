import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog
from PIL import Image, ImageTk
import pyscreenshot
import numpy as np
import math
import random
import queue

class Turtle:
    
    def __init__(self, canvas): 
        self.canvas = canvas
        self.coords = np.array([self.canvas.winfo_width()/2, self.canvas.winfo_height()/2])
        self.load_sprite_file()
        self.load_indicator_file()
        self.load_sprite_canvas()
        self.pen_flag = True
        self.colour = '#000000'
        self.background_colour = '#FFFFFF'
        self.line_width = 1
        self.angle = 0
        self.obs_flag = False
        self.turtle_flag = False
        self.eraser_flag = False
        self.colour_old = "black"
        self.fill_flag = False
        self.fill_list = []
        self.fill_colour = "black"
        self.last_fill = None


    def ask_sprite_file(self):
        filename = filedialog.askopenfilename()
        self.load_sprite_file(filename)
        self.load_sprite_canvas() 

    def load_sprite_file(self, filename="turtle.png"):
        image = Image.open(filename)
        self.unrotatedimage = image.resize((30,int(30*image.size[1]/image.size[0])))
        self.rotatedimage = self.unrotatedimage
    
    def load_sprite_canvas(self):
        self.loadTurtle = ImageTk.PhotoImage(self.rotatedimage)
        self.turtle_sprite = self.canvas.create_image(self.coords[0],self.coords[1],anchor=tk.CENTER, image=self.loadTurtle,tag="turtle")
        self.canvas.update()
    
    def load_indicator_file(self):
        image = Image.open("squarepointer.png")
        image = image.resize((25,int(25*image.size[0]/image.size[1])),resample=Image.BICUBIC)
        self.obs_image = ImageTk.PhotoImage(image)
    
    def save_canvas(self,x,y):
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        pyscreenshot.grab((x,y,x1,y1)).save("output.png")

    def rotate(self,rel_angle):
        self.canvas.delete(self.turtle_sprite)
        self.angle+=rel_angle
        self.angle = self.angle%360
        self.rotatedimage = self.unrotatedimage.rotate(self.angle)
        #if pen is off - make turtle grayscale
        if not self.pen_flag: self.rotatedimage = self.rotatedimage.convert('LA').convert('RGBA')
        self.load_sprite_canvas()

    def move_to(self,x,y,run_over=True):
        #This is the main move function - all other move_ funcs call this 
        #Run over flag is if we want to stop the turtle crossing its own path
        crash = False
        overlap = False
        in_fill = False  
        #Using canvas item tags to detect overlaps and collisions
        overlaps = list(self.canvas.find_overlapping(self.coords[0], self.coords[1], x,y))
        for i in overlaps:
            if self.canvas.itemconfig(i)["tags"][-1] == "obstacle" or self.canvas.itemconfig(i)["tags"][-1] == "obstacle current":
                crash = True
            if self.canvas.itemconfig(i)["tags"][-1] == "fill":
                in_fill = True
        # Once an object is filled in, turtle needs to escape before it becomes an obstacle (solid)
        if not in_fill and self.last_fill:
            self.canvas.itemconfig(self.last_fill, tag="obstacle")
            self.last_fill = None
        
        # normally, turtle + line (2) but when overlapping we get more than one line (>3)
        if len(overlaps)>3 and not run_over:
            overlap = True
          
        buffer = 5 
        if not overlap and not crash and (buffer < x < self.canvas.winfo_width()-buffer) and (buffer < y < self.canvas.winfo_height()-buffer):
            if self.pen_flag: #Pen is on -> draw a line
                self.last_line = self.canvas.create_line(self.coords[0], self.coords[1], x, y, fill=self.colour, width=self.line_width, tag="line")
            self.canvas.move(self.turtle_sprite,x-self.coords[0],y-self.coords[1])
            self.last_move = self.coords
            self.coords = np.array([x,y])
            self.canvas.update() # makes movements show on canvas before main function reached again
            
            if self.fill_flag: 
                self.fill_list.append([self.coords[0],self.coords[1]])
            return True
        else: return False

    def move_inc(self,x,y,run_over=True):
        #Move function to move in increments of (roughly) 10
        #This way the turtle will stop near where it crashed, instead of staying put
        num_incs = math.ceil(np.linalg.norm(np.array([x,y])-self.coords)/10)+1
        incs = np.linspace(self.coords,np.array([x,y]),num_incs)[1:]
        for inc in incs:
            if self.move_to(inc[0],inc[1]):
                success = True 
            else: 
                success = False
                break
        return success
        
    def move(self, dir, dist=10,run_over=True):
        #convenience function for arrow key control
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

    
        
    def pen_on_off(self):
        if self.eraser_flag: #Turn off eraser if pen button is clicked
            self.eraser_on_off()
            self.pen_on_off()

        if  self.pen_flag: #pen off 
            self.canvas.delete(self.turtle_sprite)
            self.rotatedimage = self.rotatedimage.convert('LA').convert('RGBA')
            self.load_sprite_canvas()
            self.pen_flag = not self.pen_flag
        else:
            self.pen_flag = not self.pen_flag
            self.rotate(0)
        
    def eraser_on_off(self):
        if not self.pen_flag:self.pen_on_off() #Make sure pen is on to start erasing
        
        if self.eraser_flag: #Finished erasing
            self.colour = self.colour_old
            self.line_width = 1
        else: #Started erasing
            self.colour_old = self.colour
            self.line_width = 5
            self.colour = self.canvas["background"]
        self.eraser_flag = not self.eraser_flag   
    
    def set_colour(self):
        self.colour = colorchooser.askcolor(title="Pick a colour!")[1] # [1] is the hex colour
    
    def set_line_width(self):
         self.line_width = simpledialog.askinteger("Line Width", "What line width: ")

    def set_background_colour(self):
        self.background_colour = colorchooser.askcolor(title="Pick a background colour!")[1]
        self.canvas.configure(bg=self.background_colour)

    def reset(self):
        self.coords=np.array([self.canvas.winfo_width()/2, self.canvas.winfo_height()/2])
        self.canvas.delete("all")
        self.rotate(-self.angle)
        self.eraser_flag = False
        self.obs_flag = False
        self.colour = "black"
        self.background_colour = '#FFFFFF'
        self.canvas.configure(bg=self.background_colour)
        self.line_width = 1
        #self.load_sprite_canvas() loaded again in rotate

    def undo(self):
        #Currently only undoes one move
        # Could add an array of last_line objects/last_moves and move through them
        self.canvas.delete(self.last_line)
        if self.pen_flag: self.pen_on_off()
        self.move_to(self.last_move[0],self.last_move[1])
        self.pen_on_off()

    def obstacle_mouse(self,xnew,ynew):
        #This function does two things 
        # - creates obstacles when two corners are pressed
        # - moves the turtle when the turtle is pressed initially 

        # Clicked outside canvas? usually when resizing window
        if self.within_range([xnew,ynew], [0,0],[self.canvas.winfo_width()-5, self.canvas.winfo_height()-20]): 
            # Check if first or second click
            if not self.obs_flag:
                if abs(self.coords[0]-xnew)<20 and abs(self.coords[1]-ynew)<20:  #clicked on turtle?
                    self.turtle_flag = True
                else:
                    self.obs_indicator = self.canvas.create_image(self.canvas.winfo_width()-20,20,anchor=tk.CENTER, image=self.obs_image)
                    self.obstacle_coords = [xnew,ynew]
                self.obs_flag = True
            else: # Second click
                if self.turtle_flag:
                    # self.move_to(xnew,ynew)
                    self.occupancy = np.array(np.zeros([int((self.canvas.winfo_height()-10)/10)-1, int(self.canvas.winfo_width()/10)-1]),dtype=int)
                    self.go_to_a_star(int(self.coords[1]/10),int(self.coords[0]/10),int(ynew/10),int(xnew/10))
                    self.turtle_flag = False
                else:
                    # Check if new obstacle will enclose turtle
                    if not(self.within_range(self.coords,self.obstacle_coords,[xnew,ynew])): 
                        self.square_obstacle(self.obstacle_coords[0],self.obstacle_coords[1],xnew,ynew)
                    self.canvas.delete(self.obs_indicator)
                self.obs_flag = False
    
    def square_obstacle(self,x1,y1,x2,y2):
        self.canvas.create_rectangle(x1,y1,x2,y2,fill="black",tag="obstacle")
        
    def obstacle_remove(self,x,y):
        #This isnt the best way of detecting if the obstacle is clicked
        # clicking on white space near obstacle will also delete obstacle
        item = self.canvas.find_closest(x,y)
        if self.canvas.itemconfig(item)["tags"][-1] == "obstacle" or self.canvas.itemconfig(item)["tags"][-1] == "obstacle current":
            self.canvas.delete(item)
        self.obs_flag = False
        self.canvas.delete(self.obs_indicator)

     def within_range(self,check,val1,val2):
        return (val1[0]<=check[0]<=val2[0] or val2[0]<=check[0]<=val1[0]) and  (val1[1]<=check[1]<=val2[1] or val2[1]<=check[1]<=val1[1])

    def fill(self):
        #First call to function starts the move function to add moves to fill_list
        #Second call creates a polygon with those coords
        if self.fill_flag: # filling has finished
            self.fill_flag = False
            if self.fill_list != []:
                self.do_filling()
            self.fill_list = []
            self.canvas.delete(self.fill_indicator)
        else: #Started filling - show user with indicator
            self.fill_flag = True
            self.fill_indicator = self.canvas.create_oval(self.canvas.winfo_width()-50,24,self.canvas.winfo_width()-40,14,fill="black")
            
    def do_filling(self):
        #last filled object saved so turtle can escape before it becomes an obstacle
        self.last_fill = self.canvas.create_polygon(self.fill_list,fill=self.fill_colour, tag="fill")
    
    ## Shapes
    def move_square(self,d):
        if self.pen_flag: self.pen_on_off()
        # Ugly but otherwise move is too quick, 
        self.rotate(-self.angle)
        for i in range(10):
            self.move("Up",d/20)
        self.rotate(-90)
        self.pen_on_off()
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
        self.pen_on_off()
        for i in range(10):
            self.move("Down",d/20)
        self.rotate(180)
        self.pen_on_off()

    def move_circle(self,r):
        if self.pen_flag: self.pen_on_off()
        centre = self.coords
        for i in range(10):
            self.move("Up",r/10)
        self.rotate(-self.angle-90)
        self.pen_on_off()
        for i in range(361):
            x = centre[0]+r*math.sin(-i * math.pi/180+math.pi)
            y = centre[1]+r*math.cos(-i * math.pi/180+math.pi)
            self.move_to(x,y)
            self.rotate(-1)
        self.rotate(-90)
        self.pen_on_off()
        for i in range(10):
            self.move("Down",r/10)
        self.rotate(180)
        self.pen_on_off()


    def spirograph_mode(self):
        centre = self.coords
        k = random.random()
        l = random.random()
        if self.pen_flag: self.pen_on_off()
        for i in range(150):
            #Wikipedia to thank for the formula
            x = centre[0]+100*((1-k)*math.cos(i)+l*k*math.cos(i*(1-k)/k))
            y = centre[1]+100*((1-k)*math.sin(i)-l*k*math.sin(i*(1-k)/k))
            if i == 1: self.pen_on_off()
            self.move_to(x,y)
        self.pen_on_off()
        self.move_to(centre[0],centre[1])
        self.pen_on_off()
        
    def move_spiral(self):
        #Unused but does make a nice spiral
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
        #occupancy maps workspace into grid of 10 pixels
        #index [0,0] => ([idx]+1)*10 => pixel (10,10)
        self.occupancy = np.array(np.zeros([int((self.canvas.winfo_height()-10)/10)-1, int(self.canvas.winfo_width()/10)-1]),dtype=int)
        #Try to get to all points in occupancy map
        #do forward and backward pass in one go
        current = [self.coords[0],self.coords[1]]
        for i in range(0,self.occupancy.shape[0]-1,2):
            #Yes these could be put into a function and called 3 times 
            for j in range(0,self.occupancy.shape[1]):
                if not self.occupancy[i][j]:
                    if self.move_inc((j+1)*10,(i+1)*10):
                        self.occupancy[i][j] = 1
                        current = [i,j]
                    else:
                        self.occupancy[i+1][j] = 2 
                        # self.go_to_a_star(current[0],current[1],i,j)
            for j in reversed(range(0,self.occupancy.shape[1])):
                if not self.occupancy[i+1][j]:
                    if self.move_inc((j+1)*10,(i+2)*10):
                        self.occupancy[i+1][j] = 1
                        current = [i,j]
                    else:
                        self.occupancy[i+1][j] = 2 
                        # self.go_to_a_star(current[0],current[1],i,j)
        if not self.occupancy.shape[0]%2==0:
            #do remaining row if odd row number
            for j in range(0,occupancy.shape[1]):
                if not self.occupancy[-1][j]:
                    if self.move_inc((j+1)*10,(self.occupancy.shape[0])*10):
                        self.occupancy[-1][j] = 1
                        current = [i,j]
                    else:
                        self.occupancy[i+1][j] = 2 
                        # self.go_to_a_star(current[0],current[1],i,j)
    
        
    
    def go_to_a_star(self,istart,jstart,igoal,jgoal):
        frontier = queue.PriorityQueue()
        frontier.put((0,[istart,jstart]))
        came_from = dict()
        cost_so_far = dict()
        start = "{},{}".format(istart,jstart)
        came_from[start] = None
        cost_so_far[start] = 0

        neighbours = [[1,0],[0,1],[-1,0],[0,-1]]
        self.pen_on_off()
        while not frontier.empty():
            current = frontier.get()[1]
            cr = "{},{}".format(current[0],current[1])
            forward = came_from[cr]
            moves = []
            #Set pen on to draw final path
            if (current == [igoal,jgoal]):
                self.pen_on_off()
            # Move back to current
            while forward:
                moves.append(forward)
                cr = "{},{}".format(forward[0],forward[1])
                forward = came_from[cr]
            for move in reversed(moves):
                self.move_to((move[1]+1)*10,(move[0]+1)*10)
            #Exit if got to goal
            if (current == [igoal,jgoal]):
                return True
            #Try to go to all neighbours
            for next in neighbours:
                newpoint = [current[0] + next[0],current[1]+next[1]]
                cr = "{},{}".format(current[0],current[1])
                new_cost = cost_so_far[cr]+1
                if self.within_boundaries(newpoint[0],newpoint[1]):
                    #Update occupancy grid, exit if goal is in an obstacle 
                    self.is_enclosed(newpoint[0],newpoint[1])
                    if (self.occupancy[igoal][jgoal]==2):
                        self.pen_on_off()
                        return False
                    #Move to new point, and back if successful
                    if self.move_to((newpoint[1]+1)*10,(newpoint[0]+1)*10):
                        self.move_to((current[1]+1)*10,(current[0]+1)*10)
                        np = "{},{}".format(newpoint[0],newpoint[1])
                        if np not in cost_so_far or new_cost<cost_so_far[np]:
                            cost_so_far[np] = new_cost
                            priority = new_cost + self.heuristic([igoal,jgoal],newpoint)
                            frontier.put((priority,newpoint))
                            came_from[np] = current
                    else:
                        #Wasnt able to move to new point -> obstacle
                        self.occupancy[newpoint[0],newpoint[1]] = 2

            #Move back to starting point
            cr = "{},{}".format(current[0],current[1])
            back = came_from[cr]
            while back:
                self.move_to((back[1]+1)*10,(back[0]+1)*10)
                cr = "{},{}".format(back[0],back[1])
                back = came_from[cr]

        self.pen_on_off()
        return False   
            
            
    def heuristic(self,a,b):
         # Manhattan distance on a square grid
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def within_boundaries(self,i,j):
        return 0 <= i < self.occupancy.shape[0] and 0 <= j < self.occupancy.shape[1]

    def is_enclosed(self,i,j):
        occupancy_new = np.copy(self.occupancy)
        escaped=False
        while occupancy_new[i][j]!= 2:
            #This breaks if obstacle meets boundary
            if not self.within_boundaries(i,j):
                escaped = True
                break
            try: #Not the best way of including range checking
                if occupancy_new[i-1][j] !=2:
                    occupancy_new[i][j] =2
                    i-=1
                elif occupancy_new[i][j-1] !=2:
                    occupancy_new[i][j] =2
                    j-=1
                elif occupancy_new[i+1][j] !=2:
                    occupancy_new[i][j] =2
                    i+=1
                elif occupancy_new[i][j+1] !=2:
                    occupancy_new[i][j] =2
                    j+=1
                else:
                    occupancy_new[i][j] =2
            except:
                break
        if not escaped:
            self.occupancy = occupancy_new
        
        
        
        
            
            
