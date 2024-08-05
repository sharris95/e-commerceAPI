from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from dotenv import load_dotenv
import pymysql
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Gory1234!@127.0.0.1/ecommerce'  # Update with actual credentials

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

# Import pymysql and set it as MySQLdb
pymysql.install_as_MySQLdb()

# Customer Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))

    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

# CustomerAccount Model
class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    customer = db.relationship('Customer', backref=db.backref('accounts', lazy=True))

    def __init__(self, username, password, customer_id):
        self.username = username
        self.password = password
        self.customer_id = customer_id

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer)

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

    def __init__(self, order_date, customer_id):
        self.order_date = order_date
        self.customer_id = customer_id

# OrderItem Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship('Order', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

# Marshmallow Schemas
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAccount

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

# Endpoints
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.json
        if not all(key in data for key in ['name', 'email', 'phone_number']):
            return jsonify({'error': 'Missing data'}), 400

        # Check if the email already exists
        existing_customer = Customer.query.filter_by(email=data['email']).first()
        if existing_customer:
            return jsonify({'error': 'Email already exists'}), 400

        new_customer = Customer(name=data['name'], email=data['email'], phone_number=data['phone_number'])
        db.session.add(new_customer)
        db.session.commit()
        return CustomerSchema().jsonify(new_customer), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/customers/<id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        return CustomerSchema().jsonify(customer)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/customers/<id>', methods=['PUT'])
def update_customer(id):
    try:
        data = request.json
        customer = Customer.query.get_or_404(id)
        customer.name = data['name']
        customer.email = data['email']
        customer.phone_number = data['phone_number']
        db.session.commit()
        return CustomerSchema().jsonify(customer)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/customers/<id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/accounts', methods=['POST'])
def add_account():
    try:
        data = request.json
        if not all(key in data for key in ['username', 'password', 'customer_id']):
            return jsonify({'error': 'Missing data'}), 400

        new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
        db.session.add(new_account)
        db.session.commit()
        return CustomerAccountSchema().jsonify(new_account), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/accounts/<id>', methods=['GET'])
def get_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        return CustomerAccountSchema().jsonify(account)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/accounts/<id>', methods=['PUT'])
def update_account(id):
    try:
        data = request.json
        account = CustomerAccount.query.get_or_404(id)
        account.username = data['username']
        account.password = data['password']
        db.session.commit()
        return CustomerAccountSchema().jsonify(account)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/accounts/<id>', methods=['DELETE'])
def delete_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.json
        if not all(key in data for key in ['name', 'price', 'stock']):
            return jsonify({'error': 'Missing data'}), 400

        new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
        db.session.add(new_product)
        db.session.commit()
        return ProductSchema().jsonify(new_product), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get_or_404(id)
        return ProductSchema().jsonify(product)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.json
        product = Product.query.get_or_404(id)
        product.name = data['name']
        product.price = data['price']
        product.stock = data['stock']
        db.session.commit()
        return ProductSchema().jsonify(product)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def list_products():
    try:
        products = Product.query.all()
        return ProductSchema(many=True).jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders', methods=['POST'])
def place_order():
    try:
        data = request.json
        new_order = Order(order_date=datetime.utcnow(), customer_id=data['customer_id'])
        db.session.add(new_order)
        db.session.commit()
        return OrderSchema().jsonify(new_order), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<id>', methods=['GET'])
def get_order(id):
    try:
        order = Order.query.get_or_404(id)
        return OrderSchema().jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    try:
        data = request.json
        order = Order.query.get_or_404(id)
        order.order_date = datetime.strptime(data['order_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        db.session.commit()
        return OrderSchema().jsonify(order)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
