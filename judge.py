import time
import resource
import subprocess
import configparser

def check_ans(answer, target):
	answer = answer.splitlines()
	target = target.splitlines()

	if(len(answer) != len(target)):
		return False

	result = True
	for i in range(len(answer)):
		if(answer[i][-1] == " "):
			answer[i] = answer[i][:-1]
		if(target[i][-1] == " "):
			target[i] = target[i][:-1]

		result = ((answer[i].split(" ") == target[i].split(" ")) and result)

		if(not result):
			break

	return result

class Judger:
	def __init__(self, time_limit = 1, memory_limit = 1024):
		self.time_limit = time_limit
		self.memory_limit = memory_limit

		self.config = configparser.ConfigParser()
		self.config.read("config.ini", encoding = "utf-8")

	def run_code(self, filename, language, PID):
		#设置空间限制
		resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit*1024*1024, -1))


		#检查是否需要编译
		if(self.config.has_option("make", language)):
			res = subprocess.run(self.config.get("make", language).replace("#####", filename), shell = True)

			if(res.returncode != 0):
				return f"Compiling Error: {res.stderr.decode('utf-8')}"

		#记录开始时间
		start = time.time()

		#开始判题
		try:
			with open(r"./templates/problem/" + PID + r"/data/1.in", "rb") as f:
				res = subprocess.run(self.config.get("language", language).replace("#####", filename), shell = True, timeout = self.time_limit, input = f.read(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
				
				
				end = time.time()
		except subprocess.TimeoutExpired:
			return "Time Limit Exceeded!"
		
		if(res.returncode != 0):
			return f"Runtime Error: {res.stderr.decode('utf-8')}"

		answer = res.stdout.decode("utf-8")
		print(answer)

		with open(f"./templates/problem/{PID}/data/1.out", "r") as f:
			if(check_ans(answer, f.read())):
				return f"Accepted!\nExecution Time:{end-start:.2f}"
			else:
				return "Wrong answer!"
		
if(__name__ == "__main__"):
	judger = Judger(time_limit = 10)
	print(judger.run_code("./sub_code/test.py", "python3", "p1"))
