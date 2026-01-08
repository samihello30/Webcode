from flask import Blueprint, url_for, render_template, redirect, session, flash
from utils.filehandler import countdown, login_required

dash_bp = Blueprint("dash", __name__, url_prefix="/dash", template_folder="../templates/dashboard")

@dash_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=session["user"]["first_name"], timer=True)