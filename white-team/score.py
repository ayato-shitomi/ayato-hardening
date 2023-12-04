from flask import Flask, render_template, render_template_string
from flask import request

app = Flask(__name__)

yourname = "false"

# team 1 to 8
score = [False, 0, 0, 0, 0, 0, 0, 0, 0]

@app.route("/add")
def add():


@app.route("/")
def index():
	template = '''
	<html>
	<body>
		<header>
			<h1>Hardening</h1>
		</header>

		<h1>Scorebored</h1>
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
