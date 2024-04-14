import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('./Back/Online-shop.db')

# Create a cursor object
cur = conn.cursor()

# Insert 10 rows into the Users table
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE Products (
        product_id INTEGER PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )
''')

products = [
    ('Product 1', 'This is product 1 description.', 9.99, 1),
    ('Product 2', 'This is product 2 description.', 19.99, 2),
    ('Product 3', 'This is product 3 description.', 29.99, 3),
    ('Product 4', 'This is product 4 description.', 39.99, 4),
    ('Product 5', 'This is product 5 description.', 49.99, 5),
    ('Product 6', 'This is product 6 description.', 59.99, 6),
    ('Product 7', 'This is product 7 description.', 69.99, 7),
    ('Product 8', 'This is product 8 description.', 79.99, 8),
    ('Product 9', 'This is product 9 description.', 89.99, 9),
    ('Product 10', 'This is product 10 description.', 99.99, 10),
]

cursor.executemany('''
    INSERT INTO Products (name, description, price, category_id)
    VALUES (?, ?, ?, ?)
''', products)

conn.commit()
conn.close()

for i in range(11):
    i += 1
    users = [
    (i, 'user' + str(i), 'password_hash_' + str(i), 'user'+ str(i) + '@example.com', '1234567890', '2022-01-01', 'customer', None),
    ]
    cur.executemany('''
        INSERT INTO Users (user_id, username, password_hash, email, phone_number, registration_date, role, default_shipping_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)

# Commit the changes and close the connection
conn.commit()
conn.close()