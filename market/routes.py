from flask import render_template
from market import app
from market.controllers import HomeController
from flask_login import login_required
# Instantiate the controller
home_controller = HomeController()

@app.route("/")
def home_page():
    return home_controller.home()

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    return home_controller.market()
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return home_controller.register()

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return home_controller.login()

@app.route('/logout')
@login_required
def logout_page():
    print("hello logout route")
    return home_controller.logout()