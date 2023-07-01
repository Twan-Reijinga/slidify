from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

def setup_gui(bg):
	window = Tk()
	window.geometry("480x320")
	window.configure(bg = bg)

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
	return window, canvas

def display_song_text(canvas, x, y, title, artist, titleSize, artistSize):
	titleText = canvas.create_text(
		x,
		y,
		anchor="nw",
		text=title,
		fill="#000000",
		font=("Univers LT Std", titleSize)
	)
	artistText = canvas.create_text(
		x,
		y+100,
		anchor="nw",
		text=artist,
		fill="#000000",
	    font=("Univers LT Std", artistSize)
	)
	return titleText, artistText

def display_volume_text(canvas, x, y, vol, maxVol, size):
	volumeText = canvas.create_text(
		x,
		y,
		anchor="nw",
		text=f"VOL {vol}/{maxVol}",
		fill="#000000",
		font=("Arial", size)
	)
	canvas.create_rectangle(
		45.0,
		205.0,
		432.0,
		208.0,
		fill="#000000",
		outline=""
	)
	return volumeText

def volume_lines(lines, maxLines, x, y, w, h, p):
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

if __name__ == "__main__":
	window, canvas = setup_gui("#FFFFFF")
	titleText, artistText = display_song_text(canvas, 48.0, 48.0, "Song 2", "Artist Name", 96, 24)
	volumeText = display_volume_text(canvas, 48.0, 176.0, 12, 20, 20)
	volume_lines(12, 20, 48.0, 220.0, 8.0, 52.0, 8.0)
	image = PhotoImage(file=f"{Path(__file__).parent.resolve()}/assets/logo.png", width=52, height=52)
	canvas.create_image(380, 220, image=image, anchor="nw")
	# canvas.itemconfigure(titleText, text="wow")
	window.resizable(False, False)
	window.mainloop()

