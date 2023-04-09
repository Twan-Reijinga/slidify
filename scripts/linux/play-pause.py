import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

server = {
	'ip': os.getenv("SERVER_IP"),
	'user': os.getenv("SERVER_USER"),
	'port': int(os.getenv("SERVER_PORT")),
	'pass': input(f'password for {os.getenv("SERVER_USER")}: ')
}

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


exec_ssh(server, 'playerctl play-pause')


