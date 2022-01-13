import tkinter as tk

window = tk.Tk()

coords = [150, 150]

canvas = tk.Canvas(window, bg="white", height=300, width=300)
canvas.grid(column=0, row=0, columnspan=4)


def move_up():
    canvas.create_line(coords[0], coords[1], coords[0], coords[1] + 10, fill="black", width=1)
    coords[1] += 10


def move_down():
    canvas.create_line(coords[0], coords[1], coords[0], coords[1] - 10, fill="black", width=1)
    coords[1] -= 10


def move_left():
    canvas.create_line(coords[0], coords[1], coords[0] - 10, coords[1], fill="black", width=1)
    coords[0] -= 10


def move_right():
    canvas.create_line(coords[0], coords[1], coords[0] + 10, coords[1], fill="black", width=1)
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
