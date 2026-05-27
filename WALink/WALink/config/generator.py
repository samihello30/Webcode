from urllib.parse import quote_plus
from random import randint
from WALink.utills.filehandler import read_file, dump_file


def text_to_link(text, phone_number):
	while True:
		links = read_file()
		generated = randint(100000000, 999999999)
		url_text = "".join([chr(int(i)+97) for i in str(generated)])
		walink = f"https://wa.me/{phone_number}?text={quote_plus(text)}"
				
		if links:
			if next((True for f in links if f.get("link") == url_text), None):
				continue
		link = {"link_text": url_text, "link": walink}
		dump_file(add=link)
		return link.get("link_text")
