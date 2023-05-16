import os
import paramiko
from RPi import GPIO
from time import sleep
from getpass import getpass
from dotenv import load_dotenv
from rotary_encoder import setup_rotary_encoder, get_rotary_encoder_change

load_dotenv()

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

	songData['progress'] =  songData['position']/songData['length']

	return songData

def get_macos_songData(ssh):
	metadata = exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli get duration album artist title elapsedTime position')
	metadata_lines = metadata.split('\n')
	songData = {
		'length': int(float(metadata_lines[0]) * 1000),
		'album': metadata_lines[1],
		'artist': metadata_lines[2],
		'title': metadata_lines[3],
		'position': int(float(metadata_lines[4]) * 1000),
		'volume': float(exec_ssh(ssh, 'osascript -e "get volume settings"').split(',')[0].split(':')[1])
	}
	songData['progress'] =  songData['position']/songData['length']
	return songData

def get_songData(os, ssh):
	songData = {}
	if os == 'Linux':
		songData = get_linux_songData(ssh)
	elif os == 'Darwin':
		songData = get_macos_songData(ssh)
	else:
		ValueError("your OS is not yet supported")
	return songData

def play_pause_song(os, ssh):
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify play-pause')
	elif os == 'Darwin':
		exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli togglePlayPause')

def change_volume(os, ssh, volume):
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify {0}'.format(str(volume)))
	elif os == 'Darwin':
		exec_ssh(ssh, 'osascript -e "set volume output volume {0}"'.format(str(volume)))

def prev_song(os, ssh):
	if os == 'Linux':
		exec_ssh(ssh, 'playerctl -p spotify previous')
	elif os == 'Darwin':
		exec_ssh(ssh, './Documents/nowplaying-cli/nowplaying-cli previous')

if __name__ == "__main__":
	clk = 17
	dt = 18
	sw = 27
	volumeStep = 10
	prev_song(os, ssh)

	server = get_server_config()
	ssh = create_ssh_connection(server)
	server['os'] = exec_ssh(ssh, 'uname')
	songData = get_songData(server['os'], ssh)	
	print(songData)
	setup_rotary_encoder(clk, dt, sw)
	GPIO.add_event_detect(sw, GPIO.FALLING, callback=lambda x: play_pause_song(server['os'], ssh), bouncetime=200)
	while True:
		songData['volume'] += get_rotary_encoder_change(clk, dt) * volumeStep
		if songData['volume'] < 0:
			songData['volume'] = 0
		if songData['volume'] > 100:
			songData['volume'] = 100
		change_volume(server['os'], ssh, songData['volume'])
		sleep(0.01)
	

