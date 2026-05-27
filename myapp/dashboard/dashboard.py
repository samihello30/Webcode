from flask import Blueprint, url_for, render_template, redirect



@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("login_signup", option="login"))
    
    return render_template("dashboard.html", name=session["user"]["first_name"])