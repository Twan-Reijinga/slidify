from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


window = Tk()

window.geometry("480x320")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 320,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    48.0,
    176.0,
    anchor="nw",
    text="VOL 12/20",
    fill="#000000",
    font=("ArialMT", 24 * -1)
)

canvas.create_text(
    48.0,
    48.0,
    anchor="nw",
    text="Song 2",
    fill="#000000",
    font=("UniversLTStd LightUltraCn", 96 * -1)
)

canvas.create_text(
    48.0,
    131.0,
    anchor="nw",
    text="Artist Name",
    fill="#000000",
    font=("UniversLTStd LightUltraCn", 24 * -1)
)

canvas.create_rectangle(
    45.0,
    205.0,
    432.0,
    208.0,
    fill="#000000",
    outline="")
#
# canvas.create_rectangle(
#     48.0,
#     220.0,
#     322.0,
#     272.0,
#     fill="#000000",
#     outline="")
#
# canvas.create_rectangle(
#     380.0,
#     220.0,
#     432.0,
#     272.0,
#     fill="#FFFFFF",
#     outline="")
window.resizable(False, False)
window.mainloop()
