# Project Slidify

### Usecase:
The Slidify is a device meant to easily control music wirelessly from a mac/linux computer. This solves a number of problems. First, you never have to keep spotify (or other music apps) open on your computer again, because all the info can be read right from the Slidify's display. This can be handy to save screen space. Another function is to control music while your monitor is off, for when you want to work focused without distraction from your computer, for example. 


### Components
- Raspberry Pi 3b+
- 3.5 inch display
- Rotary encoder
- Motorized slider potentiometer
- Motor driver
- Battery pack
- 3D printed housing
- Power adapter
- A lot of wires


### Function
The Raspberry Pi is used to run all the code on the Slidify. It takes care of controlling the display, rotary encoder and slider. It also connects to a computer to retrieve information and execute commands.

The display is used to show all necessary music info such as: title, artist, cover image, and possibly length, album and the title and artist of the previous and next song.

The rotary encoder is used to control the dial. Turning the rotary encoder allows you to turn the volume up or down and pressing puts the song on pause/play.

The motorized slider potentiometer was the biggest inspiration for this project. It can be controlled by a motor to automatically move to the position where the song is located. The slider can detect touch and determine position. Moving it to another position will move the song to that location in the song. At the ends of the slider, I want to give the slider a counter force with the motor so that it feels a bit like a button. By moving the slider all the way to the ends it will go back or forward a song.


### Planning
##### Sprint 1 (completed):
- Ordering parts.
- Fetching data from linux to raspberry pi
- Retrieving data from macOS to raspberry pi

##### Sprint 2 (completed):
- Slider reading
- Driving the motor
- Reading a rotary encoder
- Slider button simulation at ends by driving motors

##### Sprint 3 (completed 75%): 
- Slide to right moment in song
- Control volume with rotary encoder
- Previous and next song with ends of slider
- Slide with slider to different position in song

##### Sprint 4 (in progress):
- Create UI for display
	- Design can still change but I already made a start
	- Show song image
- (opt.) Add animations to UI

##### Sprint 5:
- Designing enclosure where everything fits in
- 3D printing design

### Possible extensions:
- Making Windows compatible
- Improve UI
- Mode to integrate with spotify
	- Show Queues
	- Show album content
	- Search (and play) music
	- Add music to queue
	- Song lyrics mode
- Mode to use spotify stand alone (like an ipod)
