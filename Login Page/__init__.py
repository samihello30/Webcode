from flask import Flask
from auth.routes import auth_bp
from dashboard.routes import dash_bp
from logout.routes import logout_bp
from error.routes import error_bp
from homepage.routes import home_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "supersecretkey"
    
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(home_bp)
    
    return app