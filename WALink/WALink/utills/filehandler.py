from json import loads, dump, JSONDecodeError


def read_file(filename="walink"):
	try:
		with open(f"{filename}.json", "r") as file:
			text = file.read().strip()
			return loads(text) if text else []
	except (FileNotFoundError, JSONDecodeError):
		return []
		

def dump_file(add, filename="walink"):
	links = read_file(filename)
	try:
		with open(f"{filename}.json", "w") as file:
			links.append(add)
			dump(links, file, indent=4)
	except Exception as e:
		print("Error message: "+ str(e))