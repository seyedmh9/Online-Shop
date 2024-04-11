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

