from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font

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
	title = cut_text_at_width("Univers LT Std", titleSize, title, 400)
	titleText = canvas.create_text(
		x-10,
		y-1,
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
		x,
		y+29,
		432.0,
		y+32,
		fill="#000000",
		outline=""
	)
	return volumeText

def display_volume_lines(canvas, lines, maxLines, x, y, w, h, p):
	for line in range(maxLines):
		fill = "#000000"
		if line >= lines and line != maxLines:
			fill = "#AAAAAA"
		canvas.create_rectangle(
			x,
			y,
			x+w,
			y+h,
			fill=fill,
			outline=""
		)
		x += w + p

def display_logo(canvas, x, y, path):
	image = PhotoImage(file=f"{Path(__file__).parent.resolve()}/assets/logo.png", width=52, height=52)
	canvas.create_image(x, y, image=image, anchor="nw")
	return image

def change_song_text(canvas, titleText, artistText, title, artist):
	canvas.itemconfigure(titleText, text=title)
	canvas.itemconfigure(artistText, text=artist)

def change_volume_text(canvas, volumeText, vol, maxVol):
	canvas.itemconfigure(volumeText, text=f"VOL {vol}/{maxVol}")

def cut_text_at_width(fontType, size, text, width):
	f = font.Font(family='fontType', size=size)
	text_width = f.measure(text)
	if text_width <= width:
	    return text
	
	ellipsis = "..."
	ellipsis_width = f.measure(ellipsis)
	if ellipsis_width >= width:
	    return ellipsis
	
	cut_index = 0
	while f.measure(text[:cut_index] + ellipsis) < width:
		cut_index += 1
	
	return text[:cut_index-1] + ellipsis
	

if __name__ == "__main__":
	window, canvas = setup_gui("#FFFFFF")
	titleText, artistText = display_song_text(canvas, 48.0, 48.0, "Song 2", "Artist Name", 96, 24)
	volumeText = display_volume_text(canvas, 48.0, 176.0, 12, 20, 20)
	display_volume_lines(canvas, 12, 20, 48.0, 220.0, 8.0, 52.0, 8.0)
	image = display_logo(canvas, 380, 220, 'assets/logo.png')
	fontWidth = cut_text_at_width("Univers LT Std", 42, "HALLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", 400)
	print(fontWidth)
	window.resizable(False, False)
	window.mainloop()

