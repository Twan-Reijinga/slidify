import os
import paramiko
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

def exec_ssh(server, cmd):
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.connect(server['ip'], port=server['port'], username=server['user'], password=server['pass'])
		(stdin, stdout, stderr) = ssh.exec_command(cmd)
		cmd_out = stdout.read().decode()
		return cmd_out
	finally:
		ssh.close()

def get_song_data(server):
	metadata = exec_ssh(server, 'playerctl -p spotify metadata')
	song_data = {}
	metadata_lines = metadata.split('\n')

	for line in metadata_lines:
		line_parts = line.split()
		if 'mpris:length' in line_parts:
			song_data['length'] = int(int(line_parts[-1]) / 1000)
		elif 'xesam:album' in line_parts:
			song_data['album'] = ' '.join(line_parts[2:])
		elif 'xesam:artist' in line_parts:
			song_data['artist'] = ' '.join(line_parts[2:])
		elif 'xesam:title' in line_parts:
			song_data['title'] = ' '.join(line_parts[2:])
		elif 'xesam:url' in line_parts:
			song_data['url'] = line_parts[-1]
	song_data['position'] = exec_ssh(server, 'playerctl -p spotify position')
	song_data['volume'] = exec_ssh(server, 'playerctl -p spotify volume')
	song_data['status'] = exec_ssh(server, 'playerctl -p spotify status')

	if len(song_data) != 8:
		raise ValueError("Can't extract (part of the) song data from playerctl")
	for value in song_data.values():
		if not value:
			raise ValueError("Some part of the song data from playerctl is empty")

	return song_data


if __name__ == "__main__":
	server = {
		'ip': os.getenv("SERVER_IP"),
		'user': os.getenv("SERVER_USER"),
		'port': int(os.getenv("SERVER_PORT")),
		'pass': getpass()
	}
	song_data = get_song_data(server)
	print(song_data)

