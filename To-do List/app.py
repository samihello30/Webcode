from flask import Flask, request, redirect, url_for, render_template
from time import strftime 

all_tasks = []

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main():
    global all_tasks
    
    if request.method == "POST":
        tasks = request.form["tasks"].strip().capitalize()
        current = strftime("%I:%M %p, %d %a %b %Y")
        add_tasks = {
            tasks: current
        }
        all_tasks.append(add_tasks)
        
        if all_tasks:
            return render_template("index.html", all_tasks=all_tasks)

    return render_template("index.html", all_tasks=all_tasks)
                
@app.route("/delete/<int:id>")
def delete(id):
    global all_tasks
    
    if 0 <= id < len(all_tasks):
        all_tasks.pop(id)
     
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(debug=True)
        