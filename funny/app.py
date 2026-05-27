from flask import Flask, render_template
from time import sleep
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///funny.db"
db = SQLAlchemy(app)

class Fun(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	joke = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
	db.create_all()
	
	#fun = Fun(name="Samuel", joke="I'm a snake")
#	db.session.add(fun)
#	db.session.commit()

	#i = Fun.query.get(1)
	i = db.session.query(Fun).filter_by(name="Samuel").one_or_none()
	if i:
		print(i.id, i.name, i.joke)
	
	#funny = Fun.query.all()
#	for i in funny:
#		print(i.id, i.name, i.joke)
#	
#	if funny:
#		db.session.delete(funny[0])
#		print(funny[0].name + " has been deleted!")
		#db.session.commit()


#@app.route("/")
#def Index():
#	return render_template("index.html", countdown=countdown(10))
#	
#	
#if __name__ == "__main__":
#		app.run(debug=True, host="0.0.0.0")
		