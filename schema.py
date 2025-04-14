from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Product Model
class Product(db.Model):
	__tablename__ = 'products'
	product_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text)
	manufacturer = db.Column(db.String(255))
	price = db.Column(db.Numeric(10,2), nullable=False)
	inventory_count = db.Column(db.Integer, nullable=False)

# User Model
class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	preferences = db.Column(db.String(20), default='None')

# Products Bought Model
class ProductsBought(db.Model):
	__tablename__ = 'products_bought'
	purchase_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
	product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)
	username = db.Column(db.String(255), nullable=False)
	product_name = db.Column(db.String(255), nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	date_of_purchase = db.Column(db.DateTime, server_default=db.func.now())
