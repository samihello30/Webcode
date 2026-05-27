from flask import Blueprint, redirect
from WALink.utills.filehandler import read_file

open_bp = Blueprint("open", __name__)

@open_bp.route("/open/<link>")
def open(link):
	links = read_file()
	link = next((f for f in links if f.get("link_text") == link), None)
	if link:
		return redirect(link.get("link"))
	return links
		