import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()

canvas = tk.Canvas(window, bg="white", height=300, width=300)
canvas.grid(column=0, row=0, columnspan=4)



class Turtle:
    
    def __init__(self):
        self.coords = [150, 150]
        self.load_sprite()
        self.pen = True

    def load_sprite(self, filename="turtle.png"):
        image = Image.open(filename)
        resizeimage = image.resize((30,int(30*image.size[0]/image.size[1])))
        self.loadTurtle = ImageTk.PhotoImage(resizeimage)
        self.turtle_sprite = canvas.create_image(self.coords[0]-15,self.coords[1]-resizeimage.size[1]/2,anchor=tk.NW, image=self.loadTurtle)
    
    def move_up(self):
        #up is down!
        if self.pen:
            canvas.create_line(self.coords[0], self.coords[1], self.coords[0], self.coords[1] - 10, fill="black", width=1)
        canvas.move(self.turtle_sprite,0,-10)
        self.coords[1] -= 10


    def move_down(self):
        if self.pen:
            canvas.create_line(self.coords[0], self.coords[1], self.coords[0], self.coords[1] + 10, fill="black", width=1)
        canvas.move(self.turtle_sprite,0,10)
        self.coords[1] += 10


    def move_left(self):
        if self.pen:
            canvas.create_line(self.coords[0], self.coords[1], self.coords[0] - 10, self.coords[1], fill="black", width=1)
        canvas.move(self.turtle_sprite,-10,0)
        self.coords[0] -= 10


    def move_right(self):
        if self.pen:
            canvas.create_line(self.coords[0], self.coords[1], self.coords[0] + 10, self.coords[1], fill="black", width=1)
        canvas.move(self.turtle_sprite,10,0)
        self.coords[0] += 10

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def pen_on_off(self):
        self.pen = not self.pen

turtle = Turtle()

tk.Button(window, text="↑", command=turtle.move_up).grid(column=0, row=1)
tk.Button(window, text="↓", command=turtle.move_down).grid(column=1, row=1)
tk.Button(window, text="←", command=turtle.move_left).grid(column=2, row=1)
tk.Button(window, text="→", command=turtle.move_right).grid(column=3, row=1)
tk.Button(window, text="↰", command=turtle.turn_left).grid(column=1, row=2)
tk.Button(window, text="↱", command=turtle.turn_left).grid(column=2, row=2)
tk.Button(window, text="pen", command=turtle.pen_on_off).grid(column=0, row=2)

window.mainloop()
