from . import main
from flask import render_template

@main.app_errorhandler(404)
def error_404(error):
    return render_template("errors/404.html")

@main.app_errorhandler(500)
def error_505(error):
    return render_template("errors/500.html")