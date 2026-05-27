from random import choice 
from flask import Flask, request, url_for, redirect, render_template


determiner = {
    "Rock": "Scissors",
    "Scissors": "Paper",
    "Paper": "Rock"
}

results = {
    "wins": 0,
    "losses": 0,
    "ties": 0
  }

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    
    if request.method == "POST":
        choose = request.form["game"]
        computer = choice(["Rock", "Paper", "Scissors"])
        
        if determiner.get(choose) == computer:
            results["wins"] += 1
            outcome = "You win"
        elif determiner.get(computer) == choose:
            results["losses"] += 1
            outcome = "Computer win"
        else:
            results["ties"] += 1
            outcome = "It's a ties"
        
        for key, value in results.items():
        	if value == 5:
        		return redirect(url_for("outcome", result=key))
        return render_template("index.html", you=choose, computer=computer, outcome=outcome, wins=results["wins"], losses=results["losses"], ties=results["ties"])
        
    return render_template("index.html")
    

@app.route("/results/<result>")
def outcome(result):
    results.update({"wins": 0, "losses": 0, "ties": 0})
    if result != "ties":
        result = "You" if result == "wins" else "Computer"
        return f"{result} win the game!"
    else:
        return "It's a tie game!"
        
       
if __name__ == "__main__":
    app.run(debug=True)