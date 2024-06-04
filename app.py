import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRETKEY'

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sustainable_lifestyle_tracker.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcUrTEmAAAAADxUWt9nE_QpT7HlJp2ErwNGR1-i'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcUrTEmAAAAAIsV_TnC5TRzRFjiE3XVhwWuLG2O'

# Database Initialisation
db = SQLAlchemy(app)

from users.views import users_blueprint
from exerciseLog.views import function_blueprint
from carbonFootprint.views import carbonfootprint_blueprint

# Register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(function_blueprint)
app.register_blueprint(carbonfootprint_blueprint)


# Main Page - Home Page
@app.route('/')
def main():
    return render_template('HomePage.html')

@app.route('/services')
def services():
    return render_template('Services.html')

# Error pages
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('errorPages/404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errorPages/400.html'), 400


@app.errorhandler(403)
def forbidden_page_error(error):
    return render_template('errorPages/403.html'), 403


@app.errorhandler(500)
def internal_error(error):
    return render_template('errorPages/500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errorPages/503.html'), 503

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User


# User Loader
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    app.run()
