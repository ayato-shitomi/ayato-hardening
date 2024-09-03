import main 
import time

teams = {
	1: "11080",
	2: "12080",
	3: "13080",
	4: "14080",
	5: "15080",
	6: "16080",
	7: "17080",
	8: "18080",
}

for i in range(41):
	for i in teams:
		if main.chk_alive(i):
			main.add_score(i, 10)
	time.sleep(60)

