from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from schema import db, Product, User, ProductsBought 
import os
from dotenv import load_dotenv
import re
import secrets

load_dotenv()
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
	return render_template('index.html')

# Display route
@app.route('/display', methods=['GET', 'POST'])
def display():
	if request.method == 'POST':
		table = request.form.get('table')

		if table == 'products':
			data = Product.query.all()
			headers = ['Product ID','Name', 'Description', 'Manufacturer', 'Price', 'Inventory']
		elif table == 'users':
			data = User.query.all()
			headers = ['User ID','Username', 'Password', 'Preferences']
		elif table == 'products_bought':
			data = ProductsBought.query.all()
			headers = ['Purchase ID','Username', 'Product Name', 'Quantity', 'Date of Purchase']
		else:
			data = []
			header = []
		return render_template('display.html', data=data, headers=headers, table=table)

	return render_template('display.html', data=None, headers=None)

# Add data route
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
	if request.method == 'POST':

		table = request.form['table']

        	# Add product data
		if table == 'products':
			name = request.form['name']
			description = request.form['description']
			manufacturer = request.form['manufacturer']
			price = float(request.form['price'])
			inventory_count = int(request.form['inventory_count'])

			# Input validation
			if not re.match(r'^[a-zA-Z0-9\s]+$', name):
				flash("Invalid name", "error")
				return redirect(url_for("add_data"))
			if not isinstance(price, (float, int)) or price <= 0:
				flash("Invalid price", "error")
				return redirect(url_for("add_data"))
			if not isinstance(inventory_count, int) or inventory_count < 0:
				flash("Invalid inventory count", "error")
				return redirect(url_for("add_data"))

			new_product = Product(name=name, description=description, manufacturer=manufacturer, price=price, inventory_count=inventory_count)
			db.session.add(new_product)
			db.session.commit()

			flash(f"Product '{name}' added successfully!", "success")
			return redirect(url_for('home'))

	        # Add user data
		elif table == 'users':
			username = request.form['username']
			password = request.form['password']
			preferences = request.form['preferences']

			# Input validation
			existing_user = User.query.filter_by(username=username).first()
			if existing_user:
				flash("Username already exists. Please choose a different username.", "error")
				return redirect(url_for('add_data'))
			if not re.match(r'^[a-zA-Z0-9_]+$', username):
				flash("Invalid username", "error")
				return redirect(url_for('add_data'))
			if len(password) < 6:
				flash("Password must be at least 6 characters", "error")
				return redirect(url_for('add_data'))


			new_user = User(username=username, password=password, preferences=preferences)
			db.session.add(new_user)
			db.session.commit()

			flash(f"User '{username}' successfully added!", "success")
			return redirect(url_for('home'))

		# Add products bought data
		elif table == 'products_bought':
			user_id = int(request.form['user_id'])
			product_id = int(request.form['product_id'])
			quantity = int(request.form['quantity'])
			date_of_purchase = (request.form['date_of_purchase'])

			# Input validation
			if not isinstance(quantity, int) or quantity <= 0:
				flash("Invalid quantity")
				return redirect(url_for('add_data'))

			user = User.query.filter_by(user_id=user_id).first()
			if not user:
				flash("Invalid user ID")
				return redirect(url_for('add_data'))

			product = Product.query.filter_by(product_id=product_id).first()
			if not product:
				flash("Invalid product ID")
				return redirect(url_for('add_data'))

			new_purchase = ProductsBought(user_id=user_id, product_id=product_id, username=user.username, product_name=product.name, quantity=quantity, date_of_purchase=date_of_purchase)
			db.session.add(new_purchase)
			db.session.commit()

			flash(f"Purchase record added successfully!", "success")
			return redirect(url_for('home'))
	return render_template('add_data.html')

# Delete data route
@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
	table = request.args.get('table')
	data = []
	headers = []

	if not table:
		flash("Please select a table before deleting.", "error")
		return render_template("delete_data.html", data=data, headers=headers, table=None)

	if table == 'products':
		data = Product.query.all()
		headers = ['Product ID','Name', 'Description', 'Manufacturer', 'Price', 'Inventory']
	elif table == 'users':
		data = User.query.all()
		headers = ['User ID','Username', 'Password', 'Preferences']
	elif table == 'products_bought':
		data = ProductsBought.query.all()
		headers = ['Purchase ID','Username', 'Product Name', 'Quantity', 'Date of Purchase']

	# Handle delete request
	if request.method == 'POST':
		id = request.form['id']

		if table == 'products':
			record = Product.query.filter_by(product_id=id).first()
		elif table == 'users':
			record = User.query.filter_by(user_id=id).first()
		elif table == 'products_bought':
			record = ProductsBought.query.filter_by(purchase_id=id).first()
		else:
			record = None

		if record:
			db.session.delete(record)
			db.session.commit()
			flash(f"Record with ID {id} deleted successfully!", "success")
		else:
			flash(f"Record with ID {id} not found.", "error")
		return redirect(url_for("delete_data", table=table))

	return render_template('delete_data.html', data=data, headers=headers, table=table)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(host='0.0.0.0', port=5000, debug=True)

