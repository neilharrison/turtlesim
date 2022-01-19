import tkinter as tk
import TurtleClass as tc #tc is a bit close to tk

window = tk.Tk()
window.title("Turtle Sim")

#Make a canvas and a grid for buttons
canvas = tk.Canvas(window, bg="white", height=300, width=300)
#configure resizing 
window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
window.columnconfigure(1,weight=1)
window.columnconfigure(2,weight=1)
window.columnconfigure(3,weight=1)
canvas.grid(column=0, row=0, columnspan=5, sticky='nswe')

#Load the turtle!
turtle = tc.Turtle(canvas)

#All the keys
def keypress_manager(event):
    if event.keysym == "Left" or event.keysym == "Right" or event.keysym == "Up" or event.keysym == "Down" or event.keysym == "w" or event.keysym == "a" or event.keysym == "s" or event.keysym == "d":
        turtle.move(event.keysym)
    elif event.keysym == "e":
        turtle.rotate(-90)
    elif event.keysym == "q":
        turtle.rotate(90)
    elif event.keysym == "space":
        turtle.pen_on_off()
    elif event.keysym == "m":
        turtle.move_square(100)
    elif event.keysym == "c":
        turtle.move_circle(50)
    elif event.keysym == "h":
        turtle.hoover_mode()
    elif event.keysym == "p":
        turtle.spirograph_mode()
    elif event.keysym == "f":
        turtle.fill()
    elif event.keysym == "l":
        turtle.set_line_width()
    elif event.keysym == "b":
        turtle.set_background_colour()      
    elif event.keysym == "x":
        turtle.eraser_on_off()
    elif event.keysym == "r":
        turtle.reset()
    elif event.keysym =="Escape":
        window.destroy()
    elif event.keysym =="g":
        turtle.save_canvas(window.winfo_rootx(),window.winfo_rooty())
    elif event.keysym =="t":
        turtle.ask_sprite_file()
    elif event.keysym =="BackSpace":
        turtle.undo()

#Mouse events
def mouse_obs(event):
    turtle.obstacle_mouse(event.x,event.y)
def obs_remove(event):
    turtle.obstacle_remove(event.x,event.y)

#All the buttons
tk.Button(window, text="↑", command=lambda : turtle.move("Up")).grid(column=0, row=1)
tk.Button(window, text="↓", command=lambda : turtle.move("Down")).grid(column=1, row=1)
tk.Button(window, text="←", command=lambda : turtle.move("Left")).grid(column=2, row=1)
tk.Button(window, text="→", command=lambda : turtle.move("Right")).grid(column=3, row=1)
tk.Button(window, text="↰", command=lambda : turtle.rotate(90)).grid(column=1, row=2)
tk.Button(window, text="↱", command=lambda : turtle.rotate(-90)).grid(column=2, row=2)
tk.Button(window, text="pen", command=turtle.pen_on_off).grid(column=0, row=2)
tk.Button(window, text="colour", command=turtle.set_colour).grid(column=3, row=2)
tk.Button(window, text="line", command=turtle.set_line_width).grid(column=4, row=2)
tk.Button(window, text="□", command=lambda : turtle.move_square(100)).grid(column=1, row=3)
tk.Button(window, text="○", command=lambda : turtle.move_circle(50)).grid(column=2, row=3)
tk.Button(window, text="eraser", command=turtle.eraser_on_off).grid(column=0, row=3)
tk.Button(window, text="background", command=turtle.set_background_colour).grid(column=3, row=3)
tk.Button(window, text="fill", command=turtle.fill).grid(column=4, row=3)

#Binding events
window.bind('<Key>',keypress_manager)
canvas.bind('<Button-1>', mouse_obs)
canvas.bind('<Double-Button-1>',obs_remove)

window.mainloop()
