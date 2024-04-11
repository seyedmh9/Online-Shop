from flask import Flask, jsonify , request
import sqlite3
from flask_cors import CORS, cross_origin
import io
from datetime import datetime
from fileinput import filename 
from hashlib import md5
import random

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect("./Back/data-shop.db")
    conn.row_factory = sqlite3.Row
    return conn

# back test
@app.route('/',methods=['GET'])
def test():
    return "ok"

#-----------------user---------------------------

# users crud function
def get_all_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users')
    Users = cur.fetchall()
    final_Users = []
    for User in Users:
        final_Users.append({
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        })
    conn.close()
    return final_Users
def get_users(users_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = ?', (users_id,))
    User = cur.fetchone()
    final_users = {
            "id": User[0],
            "Name": User[1],
            "Password": User[2],
            "Email": User[3],
            "Phone": User[4],
            "registration_date": User[5],
            "Role": User[6],
            "address": User[7],
        }
    conn.close()
    return final_users
def create_user(Name, Password, Email, Phone, Role,address ):
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = md5(Password.encode()).hexdigest()
    registration_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO Users (username, password_hash,email,phone_number,registration_date,role,default_shipping_address) VALUES (?, ?, ?, ? , ?, ?, ?)', (Name, password_hash, Email, Phone, registration_date, Role,address ))
    conn.commit()
    customer_id = cur.lastrowid
    conn.close()
    return customer_id
def update_user(id,Name, Password, Email, Phone, registration_date, Role,address):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Users SET username = ?, password_hash = ?, email = ?, phone_number = ?, registration_date = ?, role = ? , default_shipping_address = ? WHERE user_id = ?', (Name, Password, Email, Phone, registration_date, Role,address,id))
    conn.commit()
    conn.close()
    return get_users(id)
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# users CRUD routes
@app.route('/Users', methods=['GET'])
def list_users():
    range = request.args.get('range')
    users = get_all_users()
    response = jsonify(users)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(users)
    return response
@app.route('/Users/<int:user_id>', methods=['GET'])
def get_customer_by_id(user_id):
    user = get_users(user_id)
    if user is None:
        return '', 404
    return jsonify(user), 200
@app.route('/Users', methods=['POST'])
def add_customer():
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    Role = request.json['Role']
    address = request.json['address']
    user_id = create_user(name, Password, Email, Phone, Role,address)
    return jsonify(get_users(user_id)), 201
@app.route('/Users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    name = request.json['Name']
    Password = request.json['Password']
    Email = request.json['Email']
    Phone = request.json['Phone']
    registration_date = request.json['registration_date']
    Role = request.json['Role']
    address = request.json['address']
    updated = update_user(user_id,name, Password, Email, Phone, registration_date, Role,address)
    return jsonify(updated), 200
@app.route('/Users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    delete_user(user_id)
    return jsonify({"id":user_id}), 200

#-----------------user---------------------------


#----------------category--------------------------

#category crud function
def get_all_Categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories')
    Categories = cur.fetchall()
    final_Categories = []
    for Categorie in Categories:
        final_Categories.append({
            "category_id": Categorie[0],
            "name": Categorie[1],
            "description": Categorie[2],
            "parent_category_id": Categorie[3],
            "created_at": Categorie[4],
        })
    conn.close()
    return final_Categories
def create_Categories(name, description, parent_category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    created_at = datetime.today().strftime('%Y-%m-%d')
    cur.execute('INSERT INTO Categories (name, description,parent_category_id,created_at) VALUES (?, ?, ?, ?)', (name, description, parent_category_id, created_at))
    conn.commit()
    conn.close()
    return "ok"
def get_Categories(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Categories WHERE category_id = ?',(id,))
    Categorie = cur.fetchone()
    conn.close()
    final_category = {
        "category_id": Categorie[0],
        "name": Categorie[1],
        "description": Categorie[2],
        "parent_category_id": Categorie[3],
        "created_at": Categorie[4],
    }
    return final_category
def delete_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Categories WHERE category_id = ?', (id,))
    conn.commit()
    conn.close()
def update_category(name,description,parent_category_id,created_at,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE Categories SET name = ?, description = ?, parent_category_id = ?, created_at = ? WHERE category_id = ?', (name,description,parent_category_id,created_at,id))
    conn.commit()
    conn.close()
    return get_Categories(id)

# category crud routes
@app.route('/Categories', methods=['GET'])
def list_Categories():
    Categories = get_all_Categories()
    response = jsonify(Categories)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(Categories)
    return response
@app.route('/Category/<int:id>', methods=['GET'])
def Category(id):
    Category = get_Categories(id)
    if Category is None:
        return '', 404
    return jsonify(Category), 200
@app.route('/Categories', methods=['POST'])
def add_Categories():
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    Categories_id = create_Categories(name, description, parent_category_id)
    return "ok", 201
@app.route('/Category/<int:id>', methods=['DELETE'])
def delete_category_by_id(id):
    delete_category(id)
    return jsonify({"id":id}), 200
@app.route('/Category/<int:id>', methods=['PUT'])
def update_category_by_id(id):
    name = request.json['name']
    description = request.json['description']
    parent_category_id = request.json['parent_category_id']
    created_at = request.json['created_at']
    updated = update_category(name, description, parent_category_id, created_at,id)
    return jsonify(updated), 200

#----------------category--------------------------
#------------------order--------------------------
#order crud function
def get_all_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders')
    orders = cur.fetchall()
    final_orders = []
    for order in orders:
        final_orders.append({
            "order_id": order[0],
            "user_id": order[1],
            "order_date": order[2].strftime('%Y-%m-%d %H:%M:%S'),
            "total_amount": order[3],
            "status": order[4],
    })
    conn.close()
    return final_orders
def create_order(user_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)', (user_id, order_date_str, total_amount, status))
    conn.commit()
    conn.close()
    return "ok"
def get_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders WHERE order_id = ?', (order_id,))
    order = cur.fetchone()
    conn.close()
    if order is None:
        return None
    return {
        "order_id": order[0],
        "user_id": order[1],
        "order_date": order[2].strftime('%Y-%m-%d %H:%M:%S'),
        "total_amount": order[3],
        "status": order[4],
    }
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM Orders WHERE order_id = ?', (order_id,))
    conn.commit()
    conn.close()
    return "ok"
def update_order(order_id, customer_id, order_date, total_amount, status):
    conn = get_db_connection()
    cur = conn.cursor()
    update_stmt = "UPDATE Orders SET "
    update_params = []
    if customer_id is not None:
        update_stmt += "customer_id = ?, "
        update_params.append(customer_id)
    if order_date is not None:
        order_date_str = order_date.strftime('%Y-%m-%d %H:%M:%S')
        update_stmt += "order_date = ?, "
        update_params.append(order_date_str)        
#order crud routes
@app.route('/orders', methods=['GET'])
def list_orders():
    orders = get_all_orders()
    response = jsonify(orders)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(orders)
    return response
@app.route('/Order/<int:order_id>', methods=['GET'])
def order(order_id):
    order = get_order(order_id)
    if order is None:
        return '', 404
    return jsonify(order), 200
@app.route('/Orders', methods=['POST'])
def add_order():
    user_id = request.json['customer_id']
    order_date_str = request.json['order_date']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    order_id = create_order(user_id, order_date, total_amount, status)
    return jsonify({"order_id": order_id}), 201
@app.route('/Order/<int:order_id>', methods=['DELETE'])
def delete_order_by_id(order_id):
    delete_order(order_id)
    return jsonify({"id": order_id}), 200
@app.route('/Order/<int:order_id>', methods=['PUT'])
def update_order_by_id(order_id):
    user_id = request.json['customer_id']
    order_date_str = request.json['order_date']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
    total_amount = request.json['total_amount']
    status = request.json['status']
    updated_order = update_order(order_id, user_id, order_date, total_amount, status)
    return jsonify(updated_order), 200

#------------------order--------------------------
