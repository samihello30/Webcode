from flask import Blueprint, url_for, redirect, session, flash

logout_bp = Blueprint("out", __name__, url_prefix="/logout")

@logout_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login_signup", option="login"))