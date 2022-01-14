import tkinter as tk
import TurtleClass as tc #tc is a bit close to tk

window = tk.Tk()
window.title("Turtle Sim")

canvas = tk.Canvas(window, bg="white", height=300, width=300)
canvas.grid(column=0, row=0, columnspan=4)

turtle = tc.Turtle(canvas)

tk.Button(window, text="↑", command=lambda : turtle.move("Up")).grid(column=0, row=1)
tk.Button(window, text="↓", command=lambda : turtle.move("Down")).grid(column=1, row=1)
tk.Button(window, text="←", command=lambda : turtle.move("Left")).grid(column=2, row=1)
tk.Button(window, text="→", command=lambda : turtle.move("Right")).grid(column=3, row=1)
tk.Button(window, text="↰", command=lambda : turtle.rotate(90)).grid(column=1, row=2)
tk.Button(window, text="↱", command=lambda : turtle.rotate(-90)).grid(column=2, row=2)
tk.Button(window, text="pen", command=turtle.pen_on_off).grid(column=0, row=2)
tk.Button(window, text="colour", command=turtle.pick_colour).grid(column=3, row=2)


window.mainloop()
