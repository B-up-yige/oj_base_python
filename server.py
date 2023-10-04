from flask import Flask, abort, request, render_template
from configparser import ConfigParser
import judge
import time

#初始化配置文件
config = ConfigParser()
config.read("config.ini", encoding = "utf-8")

#初始化框架
app = Flask(__name__)

#静态网页访问
@app.route("/")
@app.route("/<path:path>")
def normal(path = "index.html"):
	try:
		return render_template(path)
	except:
		abort(404)

#题目集访问
@app.route("/problem/<PID>")
def problem(PID):
	try:
		return render_template(f"/problem/{PID}/{PID}.html")
	except:
		abort(404)

#登录接口
@app.route("/login", methods = ["GET", "POST"])
def login():
	if(request.method == "GET"):
		return render_template("login.html")
	else:
		name, pwd = request.form["name"], request.form["pwd"]
		with open("login_log.txt", "a") as f:
			f.write(f"{name} use password <{pwd}> to login\n")

		return "Accepted"

#判题接口
@app.route("/problem/<PID>/submit/", methods = ["POST"])
def submit(PID):
	if(request.method == "POST"):
		f = request.files["file"]
		if(f):
			filename = r"sub_code/"+str(time.time())
			f.save(filename)

			judger = judge.Judger()
			return judger.run_code(filename, request.form["language"], PID)
		else:
			return "!QAQ!"

if(__name__ == "__main__"):
	app.run(host = "0.0.0.0", port = int(config.get("Base", "port")))
