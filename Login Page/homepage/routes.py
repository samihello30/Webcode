from flask import Blueprint, render_template, redirect, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def homepage():
    return redirect(url_for("auth.login_signup", option="login"))
    