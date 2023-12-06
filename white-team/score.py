from flask import Flask, render_template, render_template_string
from flask import request

app = Flask(__name__)

yourname = "false"

# team 1 to 8
score = [False, 0, 0, 0, 0, 0, 0, 0, 0]

@app.route("/add")
def add():
	global score
	get_team = request.args.get('team')
	get_score = request.args.get('score')
	print(get_team, get_score)
	if get_team is not None and get_score is not None:
		score[int(get_team)] += int(get_score)
	return score

@app.route("/")
def index():
	template = '''
	<html>
	<body>
		<header>
			<meta http-equiv="refresh" content="5; URL=./">
			<link rel="stylesheet" href="./static/css/style.css">
		</header>
		<h1>Scoreboard</h1>
		<table>
			<tr><th>Team</th><th>Score</th></tr>
			<tr><td>Team 1</td><td>{}</td></tr>
			<tr><td>Team 2</td><td>{}</td></tr>
			<tr><td>Team 3</td><td>{}</td></tr>
			<tr><td>Team 4</td><td>{}</td></tr>
			<tr><td>Team 5</td><td>{}</td></tr>
			<tr><td>Team 6</td><td>{}</td></tr>
			<tr><td>Team 7</td><td>{}</td></tr>
			<tr><td>Team 8</td><td>{}</td></tr>
		</table>
	</body>
	</html>
	'''.format(score[1], score[2], score[3], score[4], score[5], score[6], score[7], score[8])
	return render_template_string(template)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=80)
