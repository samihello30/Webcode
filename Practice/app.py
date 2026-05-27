from flask import Flask, url_for, render_template, session, flash, redirect, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("error.html", code=e.code, description=e.description), e.code


#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template("404.html"), 404


#@app.errorhandler(500)
#def internal_serve(error):
#    return render_template("500.html"), 500
#    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Please enter username!", "error")
            return redirect(url_for("login"))
        
        session["user"] = username
        flash("Login successfully", "success")
        return redirect(url_for("dashboard", username=session["user"]))
    
    return render_template("index.html")


@app.route("/dashboard/<username>") 
def dashboard(username):
    if "user" not in session:
        flash("You must login first!", "error")
        return redirect(url_for("login"))
    
    return render_template("dashboard.html", username=username)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

      
if __name__ == "__main__":
    app.run(debug=True)