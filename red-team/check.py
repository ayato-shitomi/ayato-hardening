import main 
import time

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

for i in range(41):
	for i in teams:
		ip = teams[i]
		if main.chk_alive(i):
			main.add_score(i, 10)
	time.sleep(60)

