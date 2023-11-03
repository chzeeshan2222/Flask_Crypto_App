from flask import render_template, redirect, url_for, flash,request,jsonify
from market.models import items, User
from market.forms import RegisterForm, LoginForm,PurchaseItemForm,SellItemForm
from market import db,app
from flask_login import login_user,logout_user,login_required,current_user

class HomeController:
    def home(self):
        print("Home Page")
        return render_template('home.html')

    def market(self):
        print("Market Page")
        purchase_form = PurchaseItemForm()
        selling_form=SellItemForm()
        if request.method == "POST":
            purchased_item = request.form.get('purchased_item')
            p_item_object = items.query.filter_by(name=purchased_item).first()

            if p_item_object:
                if current_user.can_purchase(p_item_object):
                    p_item_object.buy(current_user)
                    p_item_object.owner = current_user.username  # Change the owner to the current user
                    db.session.commit()

                    flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                          category='success')
                    return redirect(url_for('market_page'))
                else:
                    flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!",
                          category='danger')
                    return redirect(url_for('market_page'))
                   # Sell Item Logic

            sold_item = request.form.get('sold_item')
            print(sold_item)
            s_item_object = items.query.filter_by(name=sold_item).first()
            print(f"after database in obj {s_item_object}")
            #
            print(f"after database in current {current_user.can_sell(s_item_object)}")
            if s_item_object:
                print(f"outer if{s_item_object}")
                if current_user.can_sell(s_item_object):
                   # print(f" inside if{s_item_object.sell(current_user)}")
                    s_item_object.sell(current_user)
                    flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
                else:
                    flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
            return redirect(url_for('market_page'))
        if request.method == "GET":
            # Fetch items not owned by the current user
            owned_items = items.query.filter_by(owner=current_user.username).all()
            item_test = items.query.filter_by(owner=None)
            print(owned_items)
            return render_template('market.html', items=item_test, purchase_form=purchase_form,selling_form=selling_form,owned_items=owned_items)

    def register(self):
        form = RegisterForm()
        if form.validate_on_submit():
            user_to_create = User(
                username=form.username.data,
                email_address=form.email_address.data,
                password=form.password1.data
            )
            with app.app_context():
                db.session.add(user_to_create)
                db.session.commit()
            flash(f'Registered successfully!', category='success')  # Flash success message
            return redirect(url_for('market_page'))

        if form.errors:  # If there are errors from the validations
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')

        return render_template('forms.html', form=form)

    def login(self):
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('market_page'))
            else:
                flash('Username and password do not match! Please try again', category='danger')

        return render_template('login.html', form=form)
    def logout(self):

        # if current_user.is_authenticated:  # Check if the user is authenticated before logging out
        logout_user()
        print("logout Controller")
        flash("You have been logged out!", category='info')
        return redirect(url_for("home_page"))

    def create_product(self):
        data = request.get_json()  # Get JSON data from the request

        # Extract product details from the JSON data
        name = data.get('name')
        price = data.get('price')
        barcode = data.get('barcode')
        description = data.get('description')

        if not all([name, price, barcode, description]):
            return jsonify({'error': 'Incomplete data provided'}), 400

        # Create a new item
        new_item = items(
            name=name,
            price=price,
            barcode=barcode,
            description=description
        )

        try:
            with app.app_context():
                # Add the new item to the session
                db.session.add(new_item)

                # Commit the changes to the database
                db.session.commit()

                return jsonify({'message': 'Product added successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update_item(self, item_id, data):
        item = items.query.get_or_404(item_id)

        if data.get('name'):
            item.name = data['name']

        if data.get('price'):
            item.price = data['price']

        if data.get('barcode'):
            item.barcode = data['barcode']

        if data.get('description'):
            item.description = data['description']

        db.session.commit()

        return {'message': f'Item {item_id} has been updated.'}, 200

    def delete_item(self, item_id):
        # Logic to delete the item with ID item_id from the database
        # Perform the deletion operation using your ORM or database library
        item = items.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        return f"Item with ID {item_id} deleted successfully"