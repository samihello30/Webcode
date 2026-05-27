from flask import Flask, url_for, render_template, session, flash, redirect, request
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")