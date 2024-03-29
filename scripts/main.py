import os
import paramiko
from RPi import GPIO
import time
from getpass import getpass
from dotenv import load_dotenv
from rotary_encoder import setup_rotary_encoder, handle_rotary_encoder_change
from MCP3008 import setup_MCP3008, get_analog_value
from motor_control import setup_motor, slide_to_value
from gui.main import * 	

load_dotenv()
songData = []

def get_server_config():
	server = {
		'ip': os.getenv("SERVER_IP"),
		'user': os.getenv("SERVER_USER"),
		'port': int(os. getenv("SERVER_PORT", 22)),
		'pass': getpass()
	}
	for value in server.values():
		if not value:
			raise ValueError("Not all environment variables are filled in")
	return server

def create_ssh_connection(server):
	ssh = paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.connect(server['ip'], port=server['port'], username=server['user'], password=server['pass'])
	return ssh

def exec_ssh(ssh, cmd):
	(stdin, stdout, stderr) = ssh.exec_command(cmd)
	cmd_out = stdout.read().decode()
	if cmd_out and cmd_out[-1] == '\n':
		cmd_out = cmd_out[0:-1]
	return cmd_out

def get_linux_songData(ssh):
	metadata = exec_ssh(ssh, 'playerctl -p spotify metadata')
	songData = {}
	metadata_lines = metadata.split('\n')

	for line in metadata_lines:
		line_parts = line.split()
		if 'mpris:length' in line_parts:
			songData['length'] = int(int(line_parts[-1]) / 1000)
		elif 'xesam:album' in line_parts:
			songData['album'] = ' '.join(line_parts[2:])
		elif 'xesam:artist' in line_parts:
			songData['artist'] = ' '.join(line_parts[2:])
		elif 'xesam:title' in line_parts:
			songData['title'] = ' '.join(line_parts[2:])
		elif 'xesam:url' in line_parts:
			songData['url'] = line_parts[-1]
	songData['position'] = int(float(exec_ssh(ssh, 'playerctl -p spotify position')) * 1000)
	songData['volume'] = float(exec_ssh(ssh, 'playerctl -p spotify volume'))
	songData['status'] = exec_ssh(ssh, 'playerctl -p spotify status')

	if len(songData) != 8:
		raise ValueError("Can't extract (part of the) song data from playerctl")
	for value in songData.values():
		if not value:
			raise ValueError("Some part of the song data from playerctl is empty")
	return songData

def get_macos_songData(ssh):
	metadata = exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli get duration album artist title')
	metadata_lines = metadata.split('\n')
	songData = {
		'length': int(float(metadata_lines[0]) * 1000),
		'album': metadata_lines[1],
		'artist': metadata_lines[2],
		'title': metadata_lines[3],
		'position': int(float(exec_ssh(ssh, "osascript -e 'tell application \"Spotify\" to player position'")) * 1000),
		'volume': float(exec_ssh(ssh, 'osascript -e "output volume of (get volume settings)"'))/100
	}
	return songData

def get_songData(os, ssh):
	songData = {}
	if os == 'Linux':
		songData = get_linux_songData(ssh)
	elif os == 'Darwin':
		songData = get_macos_songData(ssh)
	else:
		raise ValueError("your OS is not yet supported")
	songData['title'] = cut_text_at_width("Univers LT Std", 96, songData['title'], 400)
	return songData

def play_pause_song(os, ssh):
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify play-pause')
	elif os == 'Darwin':
		exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli togglePlayPause')

def get_volume(os, ssh):
	volume = -1
	if os == 'Linux':
		volume = float(exec_ssh(ssh, 'playerctl -p spotify volume'))
	if os == 'Darwin':
		volume = float(exec_ssh(ssh, 'osascript -e "output volume of (get volume settings)"'))/100
	return volume


def change_volume(os, ssh, volumeChange, canvas, volumeText):
	action = "+"
	if volumeChange < 0:
		action = "-"
		volumeChange *= -1

	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify volume {}{}'.format(volumeChange, action))
	elif os == 'Darwin':
		exec_ssh(ssh, 'osascript -e "set volume output  volume ((output volume of (get volume settings)) {} {}*100)"'.format(action, volumeChange))
	
	volume = get_volume(os, ssh)
	volumeStep = round(round(volume,2)/volumeChange)
	maxVolumeStep = int(1/volumeChange)
	change_volume_text(canvas, volumeText, volumeStep, maxVolumeStep)
	display_volume_lines(canvas, volumeStep, maxVolumeStep, 48.0, 220.0, 8.0, 52.0, 8.0)


def change_song(os, ssh, action):
	if not action == 'previous' and not action == 'next':
		raise ValueError('change_song action not supported')
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify {}'.format(action))
	elif os == 'Darwin':
		exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli {}'.format(action))

def change_song_position(os, ssh, position):
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify position {}'.format(str(position)))
	else:
		print("position to {}: changing position is not yet supported on your system".format(str(position)))

def update_song_data(os, ssh, window, canvas, titleText, artistText, songUpdateFreq):
	global songData
	songData = get_songData(os, ssh)	
	change_song_text(canvas, titleText, artistText, songData['title'], songData['artist'])
	window.after(songUpdateFreq, lambda: update_song_data(os, ssh, window, canvas, titleText, artistText, songUpdateFreq))

def update_slider(os, ssh, window, sliderUpdateFreq, channel, clk, Dout, Din, cs, in1, in2, pwm):
	global songData
	songData['position'] += sliderUpdateFreq
	progress = songData['position']/songData['length']
	if songData['position'] > songData['length']:
		songData = get_songData(os, ssh)	
	sliderPosition = get_analog_value(channel, clk, Dout, Din, cs)
	if(sliderPosition < 50):
		change_song(os, ssh, 'previous')
		slide_to_value(90, sliderPosition, in1, in2, pwm)
		time.sleep(sliderUpdateFreq/1000)
	elif(sliderPosition > 1960):
		change_song(os, ssh, 'next')
		slide_to_value(0, sliderPosition, in1, in2, pwm)
		time.sleep(sliderUpdateFreq/1000)
	#print(f"slider_position: {sliderPosition} - progress {progress}")
	toValue = 80 + int(progress * 1850)
	slide_to_value(toValue, sliderPosition, in1, in2, pwm)
	window.after(sliderUpdateFreq, lambda: update_slider(os, ssh, window, sliderUpdateFreq, channel, clk, Dout, Din, cs, in1, in2, pwm))

def main():
	global songData
	songUpdateFreq = 2000
	sliderUpdateFreq = 100
	volumeStep = 0.05
	rotaryClk = 0
	rotaryDt = 1
	rotarySw = 5
	adcClk = 12
	adcDout = 16
	adcDin = 20
	adcCs = 21
	adcChannel = 0
	in1 = 19
	in2 = 13
	en = 26

	window, canvas = setup_gui("#FFFFFF")

	# config	
	server = get_server_config()
	ssh = create_ssh_connection(server)
	server['os'] = exec_ssh(ssh, 'uname')
	songData = get_songData(server['os'], ssh)	

	# gpio pins
	pwm = setup_motor(in1, in2, en)
	GPIO.setwarnings(False)
	setup_MCP3008(adcClk, adcDout, adcDin, adcCs)
	setup_rotary_encoder(rotaryClk, rotaryDt, rotarySw)

	# gui
	titleText, artistText = display_song_text(canvas, 48.0, 48.0, songData['title'], songData['artist'], 96, 24)
	volumeText = display_volume_text(canvas, 48.0, 176.0, 12, 20, 20)
	display_volume_lines(canvas, 12, 20, 48.0, 220.0, 8.0, 52.0, 8.0)
	image = display_logo(canvas, 380, 220, 'assets/logo.png')
	window.attributes("-fullscreen", True)

	# GPIO events
	handle_rotary_encoder_change(rotaryClk, rotaryDt, change_volume, server['os'], ssh, volumeStep, canvas, volumeText)
	GPIO.add_event_detect(rotarySw, GPIO.FALLING, callback=lambda x: play_pause_song(server['os'], ssh), bouncetime=200)

	window.after(songUpdateFreq, lambda: update_song_data(server['os'], ssh, window, canvas, titleText, artistText, songUpdateFreq))
	window.after(sliderUpdateFreq, lambda: update_slider(server['os'], ssh, window, sliderUpdateFreq, adcChannel, adcClk, adcDout, adcDin, adcCs, in1, in2, pwm))
	window.mainloop()
	
	prevTime = time.time()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pwm.stop()
		GPIO.cleanup()
		exit()

	

