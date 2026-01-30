import sqlite3

# Step 1: Establish a connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Step 2: Create the accounts table (with phone_number included)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number TEXT,
        cvv TEXT,
        expiry_date TEXT,
        password TEXT,
        name TEXT,
        phone_number TEXT  -- Phone number column included
    )
''')

# Step 3: Create the fingerprints table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fingerprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        fingerprint_image BLOB,
        fingerprint_name TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
''')

# Step 4: Commit the changes and close the connection
conn.commit()
conn.close()

print("Database with phone_number column created successfully.")
