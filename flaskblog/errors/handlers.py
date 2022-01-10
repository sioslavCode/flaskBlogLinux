from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)  # Page not found
def error_404(error):
    return render_template('errors/404.html'), 404  # U flasku trebamo vratiit i 404 )defaul je 200 OK


@errors.app_errorhandler(403)  # No perrmision error
def error_403(error):
    return render_template('errors/403.html'), 403  # U flasku trebamo vratiit i 404 )defaul je 200 OK


@errors.app_errorhandler(500)  # General erroe
def error_500(error):
    return render_template('errors/500.html'), 500  # U flasku trebamo vratiit i 404 )defaul je 200 OK
