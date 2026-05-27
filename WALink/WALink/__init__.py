from flask import Flask, Blueprint
from WALink.link_generator.routes import whatsapp_link_bp
from WALink.open.routes import open_bp

def create_app():
	app = Flask(__name__)
	app.secret_key = "superkey"
	app.register_blueprint(whatsapp_link_bp)
	app.register_blueprint(open_bp)
	
	return app
	