E-commerce API

Project Overview

Welcome to my E-commerce API project! This project is part of my full-stack coding bootcamp, where I've been learning to build web applications using Flask and Flask-SQLAlchemy. The API is designed to handle basic e-commerce functionalities, like managing customers, products, and orders. This project is a great way for me to apply what I've learned about RESTful APIs, databases, and backend development.

Features

Customer Management: Add, view, update, and delete customers.
Product Management: Manage products in the catalog.
Order Management: Handle customer orders, including placing and viewing orders.
Setup and Installation
Prerequisites
Before getting started, make sure you have the following installed:

Python 3.11
MySQL
pip (Python package installer)

Installation

Clone the repository:



git clone <repository-url>
cd <repository-directory>

Create a virtual environment:



python -m venv venv

Activate the virtual environment:

On Windows:


venv\Scripts\activate
On macOS/Linux:


source venv/bin/activate
Install the required packages:



pip install -r requirements.txt
Environment Setup
Create a .env file in the project root directory with the following content:



SQLALCHEMY_DATABASE_URI=mysql+pymysql://<username>:<password>@localhost/ecommerce
Replace <username> and <password> with your MySQL credentials.

Initialize the database:



flask db init
flask db migrate -m "Initial migration."
flask db upgrade
Running the Server
Start the Flask server:


flask run
The API will be running at http://127.0.0.1:5000/.
API Endpoints
Customer Management
Create Customer

POST /customers
Body:


{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "123-456-7890"
}
Response:


{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "123-456-7890"
}
Get Customer by ID

GET /customers/<id>
Response:


{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone_number": "123-456-7890"
}
Update Customer

PUT /customers/<id>
Body:


{
    "name": "John Doe Jr.",
    "email": "john.doe.jr@example.com",
    "phone_number": "123-456-7890"
}
Response:


{
    "id": 1,
    "name": "John Doe Jr.",
    "email": "john.doe.jr@example.com",
    "phone_number": "123-456-7890"
}
Delete Customer

DELETE /customers/<id>
Response:


{
    "message": "Customer deleted"
}
Product Management
Create Product

POST /products
Body:


{
    "name": "Product Name",
    "price": 19.99,
    "stock": 100
}
Response:


{
    "id": 1,
    "name": "Product Name",
    "price": 19.99,
    "stock": 100
}
Get Product by ID

GET /products/<id>
Response:


{
    "id": 1,
    "name": "Product Name",
    "price": 19.99,
    "stock": 100
}
Update Product

PUT /products/<id>
Body:


{
    "name": "Updated Product Name",
    "price": 24.99,
    "stock": 150
}
Response:


{
    "id": 1,
    "name": "Updated Product Name",
    "price": 24.99,
    "stock": 150
}
Delete Product

DELETE /products/<id>
Response:


{
    "message": "Product deleted"
}
List Products

GET /products
Response:


[
    {
        "id": 1,
        "name": "Product Name",
        "price": 19.99,
        "stock": 100
    },
    ...
]
Order Management
Place Order

POST /orders
Body:


{
    "customer_id": 1,
    "products": [
        { "product_id": 1, "quantity": 2 },
        { "product_id": 2, "quantity": 1 }
    ]
}
Response:


{
    "id": 1,
    "order_date": "2024-08-05T10:00:00.000000Z",
    "customer_id": 1,
    ...
}
Get Order by ID

GET /orders/<id>
Response:


{
    "id": 1,
    "order_date": "2024-08-05T10:00:00.000000Z",
    "customer_id": 1,
    ...
}

Update Order

PUT /orders/<id>
Body:


{
    "order_date": "2024-08-06T10:00:00.000000Z"
}
Response:


{
    "id": 1,
    "order_date": "2024-08-06T10:00:00.000000Z",
    ...
}
Delete Order

DELETE /orders/<id>
Response:


{
    "message": "Order deleted"
}

Environment Variables

SQLALCHEMY_DATABASE_URI: The URI for connecting to the MySQL database.

GitHub Repository

Link to GitHub Repository (https://github.com/sharris95/e-commerceAPI)

Known Issues and Future Enhancements

Known Issues:

Some error messages might not be very descriptive.
Currently, there's no user authentication or authorization.

Future Enhancements
Add user authentication and authorization features.
Implement additional features like managing product stock levels and order tracking.
Improve error handling and validation feedback.
