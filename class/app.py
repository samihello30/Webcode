from flask import Flask, render_template, request
from filehandler import FileHandler


class FunProject:
	def __init__(self):
		self.app = Flask(__name__)
		self.db = FileHandler("h.json")
		self.data = self.db.read()
		if not self.data: self.data = []
		
	def add_member(self, request):
		self.data.append(request)
		self.db.save(self.data)
	
	def run_webcode(self):
		@self.app.route("/", methods=["POST", "GET"])
		def main():
			if request.method == "POST":
				self.add_member(request.form)
				return self.data
			return render_template("index.html")
		self.app.run(debug=True, host="0.0.0.0")

if __name__ == "__main__":
	fun = FunProject()
	fun.run_webcode()
	fun.greeting()



