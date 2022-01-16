import tkinter as tk
import TurtleClass as tc #tc is a bit close to tk

window = tk.Tk()
window.title("Turtle Sim")

canvas = tk.Canvas(window, bg="white", height=300, width=300)
canvas.grid(column=0, row=0, columnspan=4)

turtle = tc.Turtle(canvas)

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
        turtle.move_square(50)
    elif event.keysym == "c":
        turtle.move_circle(50)
    elif event.keysym == "r":
        turtle.reset()
    elif event.keysym =="Escape":
        window.destroy()

def mouse_obs(event):
    turtle.obstacle_mouse(event.x,event.y)
def obs_remove(event):
    turtle.obstacle_remove(event.x,event.y)


tk.Button(window, text="↑", command=lambda : turtle.move("Up")).grid(column=0, row=1)
tk.Button(window, text="↓", command=lambda : turtle.move("Down")).grid(column=1, row=1)
tk.Button(window, text="←", command=lambda : turtle.move("Left")).grid(column=2, row=1)
tk.Button(window, text="→", command=lambda : turtle.move("Right")).grid(column=3, row=1)
tk.Button(window, text="↰", command=lambda : turtle.rotate(90)).grid(column=1, row=2)
tk.Button(window, text="↱", command=lambda : turtle.rotate(-90)).grid(column=2, row=2)
tk.Button(window, text="pen", command=turtle.pen_on_off).grid(column=0, row=2)
tk.Button(window, text="colour", command=turtle.pick_colour).grid(column=3, row=2)

window.bind('<Key>',keypress_manager)
window.bind('<Button-1>', mouse_obs)
window.bind('<Double-Button-1>',obs_remove)

window.mainloop()
