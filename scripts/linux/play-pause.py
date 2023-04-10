import os
import paramiko
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

def exec_ssh(server, cmd):
	print('running')
	try:
		ssh = paramiko.SSHClient()
		ssh.load_system_host_keys()
		ssh.connect(server['ip'], port=server['port'], username=server['user'], password=server['pass'])
		(stdin, stdout, stderr) = ssh.exec_command(cmd)
		cmd_out = stdout.read()
		print('log printing: ', cmd, cmd_out)
		return cmd_out
	finally:
		ssh.close()

def get_song_data(server):
	metadata = exec_ssh(server, 'playerctl metadata')
	# lenght - album_title = artist - title - track_img_url

	position = exec_ssh(server, 'playerctl position')
	volume = exec_ssh(server, 'playerctl volume')
	status = exec_ssh(server, 'playerctl status')
	print(metadata, position, volume, status)


if __name__ == "__main__":
	server = {
		'ip': os.getenv("SERVER_IP"),
		'user': os.getenv("SERVER_USER"),
		'port': int(os.getenv("SERVER_PORT")),
		'pass': getpass()
	}
	get_song_data(server)

