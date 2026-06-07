from json import loads, dump, JSONDecodeError 


class FileHandler:
	def __init__(self, filename):
		self.filename = filename
	
	def read(self):	
		try:
			with open(self.filename, "r") as f:
				text = f.read().strip()
				return loads(text) if text else {}
		except (FileNotFoundError, JSONDecodeError):
			return {}
	
	def save(self, add):
		try:
			with open(self.filename, "w") as f:
				dump(add, f, indent=2)
		except Exception as e:
			print("Save File Error:", str(e))