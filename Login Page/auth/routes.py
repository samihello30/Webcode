from flask import Blueprint, url_for, render_template, session, flash, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from utils.filehandler import read_file, dump_file

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../templates/auth")

@auth_bp.route("/login_signup/<option>/<choose>", methods=["POST", "GET"])
@auth_bp.route("/login_signup/<option>", methods=["POST", "GET"])
def login_signup(option, choose=None):
    if option == "login":
        
        if request.method == "POST":
            email_phone = request.form.get("email_phone").lower().strip()
            password = request.form.get("password")
            
            if (not email_phone) or (not password):
                flash(" Enter you email or mobile number to login!" if not email_phone else "Enter email/number and password", "error")
                return redirect(url_for("auth.login_signup", option=option))
           
            users = read_file()
            if users:
                for user in users:
                    if (email_phone.lower() in [user["email_address"], user["phone_number"]]) and (check_password_hash(user["password"], password)):
                        session["user"] = user
                        flash("Logged in successfully!", "success")
                        return redirect(url_for("dash.dashboard"))
                
            flash("Incorrect email/number or password!", "error")
            return redirect(url_for("auth.login_signup", option=option))
                
        return render_template("login_signup.html", option=option)
    
    elif option == "signup":
        if choose == "email":
            return render_template("login_signup.html", option=option, email=True, choose="email")
        elif choose == "phone":
            return render_template("login_signup.html", option=option, phone=True, choose="phone")
            
        if request.method == "POST":
            first_name = request.form.get("firstName").strip()
            last_name = request.form.get("lastName").strip()
            email_address = request.form.get("email")
            phone_number = request.form.get("phone")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            checkbox = request.form.get("checkbox")
            
            if password != confirm_password:
                flash("The confirm password doesn't match the password!", "error")
                return redirect(url_for("auth.login_signup", option="signup"))
                
            user = {
              "first_name": first_name,
              "last_name": last_name,
              "email_address": email_address,
              "phone_number": phone_number,
              "password": generate_password_hash(password),
              "checkbox": checkbox
        }
        
            dump_file(dump=user)
            flash("Account created successfully!", "success")
            return redirect(url_for("auth.login_signup", option="login"))
        
        return render_template("login_signup.html", option=option, phone=True)