
from flask import Flask, render_template, render_template_string, escape
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

yourname = "false"

@app.route("/app")
def webapp():
	yourname = request.args.get('name') or ""

	template = '''
	<html>
	<head>
		<link rel="stylesheet" href="./static/css/style.css">
	</head>
	<body>
		<header>
			<h1>Fore Vietnam</h1>
			<a href="/">Home</a>
			<a href="/app?name=">Our test app</a>
		</header>

		<h1>Welcome {}, your browser infomation</h1>
		<div id="information"></div>

		<script>
			var information=document.getElementById("information");

			information.innerHTML += "host : " + location.host+"<br>";
			information.innerHTML += "host name : " + location.hostname+"<br>";
			information.innerHTML += "port : " + location.port+"<br>";
			information.innerHTML += "URL : " + location.href+"<br>";
			information.innerHTML += "protocol : " + location.protocol+"<br>";
			information.innerHTML += "search info : " + location.search+"<br>";
			information.innerHTML += "hash : " + location.hash+"<br>";
			information.innerHTML += "page URI : " + location.pathname+"<br>";
			information.innerHTML += "browser codename : " + location.appCodeName+"<br>";
			information.innerHTML += "broweser name : " + navigator.appName+"<br>";
			information.innerHTML += "brower virsion : " + navigator.appVersion+"<br>";
			information.innerHTML += "brower language : " + navigator.language+"<br>";
			information.innerHTML += "brower platform : " + navigator.platform+"<br>";
			information.innerHTML += "brower UA : " + navigator.userAgent+"<br>";
			information.innerHTML += "referrer : " + document.referrer+"<br>";
			information.innerHTML += "domain : " + document.domain+"<br>";
			information.innerHTML += "screen width : " + screen.width+"<br>";
			information.innerHTML += "screen height : " + screen.height+"<br>";
		</script>

		<footer>
			<div>Fore Vietnam</div>
			<div>Address: XXXX XXX XXXX XXX XXXXXX XXXXXXXXXXXXX</div>
			<div>Phone: +00 00 0000 0000</div>
		</footer>
	</body>
	</html>
	'''.format(yourname)
	return render_template_string(template)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=False, port=80)
