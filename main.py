import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()

coords = [150, 150]

canvas = tk.Canvas(window, bg="white", height=300, width=300)
canvas.grid(column=0, row=0, columnspan=4)

#Turtle sprite loading
image = Image.open("turtle.png")
resizeimage = image.resize((30,int(30*image.size[0]/image.size[1])))
loadTurtle = ImageTk.PhotoImage(resizeimage)
turtle = canvas.create_image(coords[0]-15,coords[1]-resizeimage.size[1]/2,anchor=tk.NW, image=loadTurtle)

def move_up():
    #up is down!
    canvas.create_line(coords[0], coords[1], coords[0], coords[1] - 10, fill="black", width=1)
    canvas.move(turtle,0,-10)
    coords[1] -= 10


def move_down():
    canvas.create_line(coords[0], coords[1], coords[0], coords[1] + 10, fill="black", width=1)
    canvas.move(turtle,0,10)
    coords[1] += 10


def move_left():
    canvas.create_line(coords[0], coords[1], coords[0] - 10, coords[1], fill="black", width=1)
    canvas.move(turtle,-10,0)
    coords[0] -= 10


def move_right():
    canvas.create_line(coords[0], coords[1], coords[0] + 10, coords[1], fill="black", width=1)
    canvas.move(turtle,10,0)
    coords[0] += 10

def turn_left():
    pass


def turn_right():
    pass

tk.Button(window, text="↑", command=move_up).grid(column=0, row=1)
tk.Button(window, text="↓", command=move_down).grid(column=1, row=1)
tk.Button(window, text="←", command=move_left).grid(column=2, row=1)
tk.Button(window, text="→", command=move_right).grid(column=3, row=1)
tk.Button(window, text="↰", command=turn_left).grid(column=1, row=2)
tk.Button(window, text="↱", command=turn_left).grid(column=2, row=2)

window.mainloop()
