from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException


error_bp = Blueprint("error", __name__, template_folder="../templates/error")

@error_bp.errorhandler(HTTPException)
def error_handler(e):
    return render_template("error.html", code=e.code, description=e.description), e.code    