import json
from functools import wraps
from flask import flash, redirect, url_for, session 
from time import sleep

def read_file(file_name="admin_manager"):
    try:
        with open(f"{file_name}.json", "r") as file:
            content = file.read().strip()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def dump_file(file_name="admin_manager", mode="new", dump=None):
    details = read_file(file_name)
    with open(f"{file_name}.json", "w") as file:
        if mode == "new":
            details.append(dump)
            json.dump(details, file, indent=4)
        elif mode == "old":
            json.dump(dump, file, indent=4)


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = f"{mins:02d}: {secs:02d}"
        print(timer, end="\r")
        sleep(1)
        t -= 1
        return timer


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if "user" not in session:
			flash("Please login first!", "error")
			return redirect(url_for("auth.login_signup", option="login"))
			
		return f(*args, **kwargs)
	return decorated_function