from flask import render_template
from market import app
from market.controllers import HomeController
from flask_login import login_required
from flask import request,jsonify
# Instantiate the controller
home_controller = HomeController()
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"page Not Found"}), 404
@app.route('/api/products', methods=['POST'])
def add_item():
    return home_controller.create_product()
@app.route('/api/update_item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    response, status_code = home_controller.update_item(item_id, data)
    return jsonify(response), status_code
@app.route('/api/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    return home_controller.delete_item(item_id)
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
