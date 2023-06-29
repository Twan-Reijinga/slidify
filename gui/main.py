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

# volume
canvas.place(x = 0, y = 0)
canvas.create_text(
    48.0,
    176.0,
    anchor="nw",
    text="VOL 12/20",
    fill="#000000",
    font=("ArialMT", 24 * -1)
)

# song name
canvas.create_text(
    48.0,
    48.0,
    anchor="nw",
    text="Song 2",
    fill="#000000",
    font=("UniversLTStd LightUltraCn", 96 * -1)
)

# artist name
canvas.create_text(
    48.0,
    131.0,
    anchor="nw",
    text="Artist Name",
    fill="#000000",
    font=("UniversLTStd LightUltraCn", 24 * -1)
)

# line
canvas.create_rectangle(
    45.0,
    205.0,
    432.0,
    208.0,
    fill="#000000",
    outline="")

# volume lines
def volume_lines(maxLines, lines, x, y, w, h, p):
	for line in range(maxLines):
		fill = "#000000"
		if line > lines:
			fill = "#DDDDDD"
		canvas.create_rectangle(
			x,
			y,
			x+w,
			y+h,
			fill=fill,
			outline=""
		)
		x += w + p

volume_lines(20, 12, 48.0, 220.0, 8.0, 52.0, 8.0)




canvas.create_rectangle(
    48.0,
    220.0,
    56.0,
    272.0,
    fill="#000000",
    outline="")
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
