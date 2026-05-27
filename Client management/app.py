import json
from time import localtime, strftime
from flask import url_for, render_template, request, redirect, Flask, flash, session


def greeter():
        current = localtime().tm_hour
        if current >= 18:
            return "Good Evening"
        elif current >= 12:
            return "Good Afternoon"
        else:
            return "Good Morning"



def read_file(file_name="client_manager_admin"):
    try:
        with open(f"{file_name}.json", "r") as file:
            content = file.read().strip()
            return json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def dump_file(file_name="client_manager_admin", mode="new", dump=None):
    details = read_file(file_name)
    with open(f"{file_name}.json", "w") as file:
        if mode == "new":
            details.append(dump)
            json.dump(details, file, indent=4)
        elif mode == "old":
            json.dump(dump, file, indent=4)



def id_generator():
    all_ids = [0]
    users = read_file()
    if users:
        for user in users:
            all_ids.append(int(user["Id"]))
    
    ids = max(all_ids)
    return f"{ids + 1:03}"



def search_client(mode, info= None):
    details = read_file()
    if details:
        for information in details:
            if info == information["Id"]:
                if mode == "search":
                    return information
                elif mode == "check":
                    return True
    else:
        return False           
                        
                                                                                                      

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def homepage():
	return render_template("index.html")
	

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        users = read_file()
        if users:
            for user in users:
                if email.lower() == "admin@gmail.com" and password == "admin owner":
                    flash("Login successfully", "success")
                    return redirect(url_for("admin"))
                elif email.lower() == user["Email Address"].lower() and password == user["Password"]:
                    session['account_owner'] = user
                    flash("Login successfully", "success")
                    return redirect( url_for("dashboard"))
                else:
                    flash("Invalid credentials", "error")
                    return redirect( url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
	session.pop("account_owner", None)
	flash("Account logged out", "success")
	return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form["firstName"].strip()
        last_name = request.form["lastName"].strip()
        email = request.form["email"].strip()
        phone_number = request.form["phone_number"].strip()
        business_name = request.form["businessname"].strip()
        password = request.form["password"].strip()
        confirm_password = request.form["confirm_password"].strip()

        users = read_file()
        for user in users:
            if user["Email Address"].lower() == email.lower():
                flash("Email already used", "error")
                return redirect(url_for("signup"))
            elif user["Phone Number"] == phone_number:
            	flash("Phone Number already used", "error")
            	return redirect(url_for("signup"))
            elif password != confirm_password:
            	flash("Unmatched password!", "error")
            	return redirect(url_for("signup"))

        new_user = {
            "First Name": first_name,
            "Last Name": last_name,
            "Email Address": email,
            "Phone Number": phone_number,
            "Business Name": business_name,
            "Password": password,
            "Join Date": strftime("%D"),
            "Id": id_generator(),
            "Data": []
        }
        dump_file(dump=new_user)
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")
    
    
@app.route("/forget-password", methods=["GET", "POST"])
def recovery():
    if request.method == "POST":
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        users = read_file()
        for user in users:
            if user["Email Address"].lower() == email.lower() and user["Phone Number"] == phone_number:
                if password == confirm_password:
                    user["Password"] = password
                    dump_file(mode="old", dump=users)
                    flash("Password updated successfully!", "success")
                    return redirect(url_for("login"))
                flash("Unmatched Password!", "error")
                return redirect(url_for("recovery"))
        flash("Invalid Credentials!", "error")
        return redirect(url_for("recovery"))
        
    return render_template("forget_password.html")

            
@app.route("/send-feedback/<mode>", methods=["GET", "POST"])
def feedback(mode=None):
    if request.method == "POST":
        full_name = request.form["fullName"].strip()
        email = request.form["email"].strip()
        message = request.form["message"].strip()
        feedbacks = {
            "Full Name": full_name,
            "Email Address": email,
            "Feedback": message
        }
        
        dump_file(file_name="feedbacks", mode="new", dump=feedbacks)
        flash("Thanks for the feedback! Your feedback means a lot for our improvement.", "success")
        
        redirects = {
                "homepage": "homepage",
                "login": "login",
                "signup": "signup",
                "recovery": "recovery",
                "dashboard": "dashboard",
                "add_client": "add_client"
            }
        if mode in redirects:
            return redirect(url_for(redirects[mode]))
        else:
            flash("Invalid feedback mode.", "error")
            return redirect(url_for("homepage"))
                        
    return render_template("feedback.html", mode=mode)
    
       
@app.route("/sub-admin/dashboard", methods=["GET", "POST"])
def dashboard():
   if "account_owner" not in session:
   	flash("Please login first!", "error")
   	return redirect(url_for("login"))
   
   return render_template("sub_admin.html", first_name=session["account_owner"] ["First Name"], current_time=greeter(), business_name=session["account_owner"] ["Business Name"])



@app.route("/sub-admin/add-client", methods=["GET", "POST"])
def add_client():
    if "account_owner" not in session:
    	flash("Please login first!", "error")
    	return redirect(url_for("login"))
    
    if request.method == "POST":
        first_name = request.form["firstName"].strip()
        last_name = request.form["lastName"].strip()
        department = request.form["department"].strip()
        matric_number = request.form["matric_number"].strip()
        topic = request.form["topic"].strip()
        phone_number = request.form["phone_number"].strip()
        
        new_client = {
            "First Name": first_name,
            "Last Name": last_name,
            "Phone Number": phone_number,
            "Department": department,
            "Matric Number": matric_number,
            "Topic": topic,
            "Total Payment": None,
            "Total Paid": [],
            "Refer": None,
            "Referred": [],
            "Referral Code": f"{first_name} {last_name} - {matric_number}",
            "Join Date": strftime("%D"),
            "Completed": None
        }
        
        users = read_file()
        for user in users:
        	if user["Email Address"].lower() == session["account_owner"] ["Email Address"].lower() and user["Phone Number"] == session["account_owner"] ["Phone Number"]:
        		user["Data"].append(new_client)
        		
        		dump_file(mode="old", dump=users)
        		session["account_owner"] = user
        		flash("New client add successful", "success")
        		return redirect(url_for("dashboard"))
        
    return render_template("add_client.html", business_name=session["account_owner"]["Business Name"])
       	
       	
       	
@app.route("/sub-admin/referral", methods=["POST", "GET"])
def refer():
    if "account_owner" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("login"))
        
    if request.method == "POST":
        first_name = request.form["firstName"].strip()
        last_name = request.form["lastName"].strip()
        phone_number = request.form["number"].strip()
        department = request.form["department"].strip()
        matric_number = request.form["matric_no"].strip()
        topic = request.form["topic"].strip()
        referred = request.form["referrer"]
        
        new_client = {
            "First Name": first_name,
            "Last Name": last_name,
            "Phone Number": phone_number,
            "Department": department,
            "Matric Number": matric_number,
            "Topic": topic,
            "Refer": referred,
            "Referred": [],
            "Referral Code": f"{first_name} {last_name} - {matric_number}",
            "Join Date": strftime("%D"),
            "Total Payment": None,
            "Total Paid": [],
            "Completed": None
        }
        
        users = read_file()
        for user in users:
        	if user["Email Address"].lower() == session["account_owner"] ["Email Address"].lower() and user["Phone Number"] == session["account_owner"] ["Phone Number"]:
        		user["Data"].append(new_client)
        		for client in user["Data"]:
        		    if referred == client["Referral Code"]:
        		        client["Referred"].append(f"{first_name} {last_name} - {matric_number}") 
        		        dump_file(mode="old", dump=users)    
                		session["account_owner"] = user
                		flash("Client referred successfully", "success")
                		return redirect(url_for("view_client"))
    
    return render_template("refer.html", users=session["account_owner"] ["Data"], business_name=session["account_owner"] ["Business Name"])
 


@app.route("/sub-admin/view_client")
def view_client():
    if "account_owner" not in session:
    	flash("Please login first!", "error")
    	return redirect(url_for("login"))
   
    return render_template("view_client.html", details=session["account_owner"] ["Data"], business_name=session["account_owner"] ["Business Name"])
    
    
    
@app.route("/sub-admin/add-info", methods=["GET", "POST"])
def add_to_info():
    if "account_owner" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        referral_code = request.form["referrer"]
        
        for found in session["account_owner"] ["Data"]: 
            if referral_code == found["Referral Code"]:
                return redirect(url_for("add_to_info", business_name=session["account_owner"] ["Business Name"], found=found))
        else:
            flash(f"{referral_code} not found", "error")
        
    return render_template("add_to_info.html", users=session["account_owner"] ["Data"], business_name=session["account_owner"] ["Business Name"])
    
    
    
@app.route("/admin/dashboard")
def admin():
    return render_template("admin.html", greeter=greeter())
    

@app.route("/admin/feedbacks")
def admin_feedbacks():
    feedbacks = read_file("feedbacks")
    return render_template("admin_feedback.html", feedbacks=feedbacks)
    

@app.route("/delete/<int:id>)")
def delete_feedbacks(id):
    feedbacks = read_file("feedbacks")
    if 0 <= id < len(feedbacks):
        feedbacks.pop(id)
        dump_file(file_name="feedbacks", mode="old", dump=feedbacks)
        flash("Feedback deleted")
        return redirect(url_for("admin_feedbacks"))
    else:
        flash("Something went wrong!")


@app.route("/about-me")
def aboutme():
	return render_template("aboutme.html")



if __name__ == "__main__":
	app.run(debug=True)