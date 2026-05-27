from flask import Blueprint, render_template, request, redirect, flash
from WALink.config.generator import text_to_link
from urllib.parse import quote_plus

whatsapp_link_bp = Blueprint("wa", __name__, template_folder="../template")

@whatsapp_link_bp.route("/", methods=["POST", "GET"])
def whatsapp_link():
	if request.method == "POST":
		details = request.form
		phone_number = details.get("phoneNumber")
		text = details.get("text")
		link = text_to_link(text, phone_number)
		flash("Link generated!", "success")
		return render_template("index.html", generated=link)
		
	return render_template("index.html")