import sqlite3

# Step 1: Establish a connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Step 2: Insert John Doe and Mary Jones into the accounts table (with phone_number)
cursor.execute("INSERT INTO accounts (account_number, cvv, expiry_date, password, name, phone_number) VALUES (?, ?, ?, ?, ?, ?)", 
               ('123456789', '123', '12/25', 'password1', 'John Doe', '+91 8097679463'))
cursor.execute("INSERT INTO accounts (account_number, cvv, expiry_date, password, name, phone_number) VALUES (?, ?, ?, ?, ?, ?)", 
               ('987654321', '456', '11/23', 'password2', 'Mary Jones', '+91 8097679463'))

# Step 3: Get the last inserted account IDs for John Doe and Mary Jones
john_doe_id = cursor.lastrowid
cursor.execute("SELECT id FROM accounts WHERE name = 'Mary Jones'")
mary_jones_id = cursor.fetchone()[0]

# Step 4: Function to read image data
def read_image(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Step 5: Insert John Doe's fingerprint images
cursor.execute("INSERT INTO fingerprints (account_id, fingerprint_image, fingerprint_name) VALUES (?, ?, ?)", 
               (john_doe_id, read_image(r'C:\Users\Krupa\Desktop\atm-simulation\fingerprint1.jpeg'), 'John Doe Fingerprint 1'))
cursor.execute("INSERT INTO fingerprints (account_id, fingerprint_image, fingerprint_name) VALUES (?, ?, ?)", 
               (john_doe_id, read_image(r'C:\Users\Krupa\Desktop\atm-simulation\fingerprint2.jpeg'), 'John Doe Fingerprint 2'))

# Step 6: Insert Mary Jones's fingerprint images
cursor.execute("INSERT INTO fingerprints (account_id, fingerprint_image, fingerprint_name) VALUES (?, ?, ?)", 
               (mary_jones_id, read_image(r'C:\Users\Krupa\Desktop\atm-simulation\fingerprint3.jpeg'), 'Mary Jones Fingerprint 1'))
cursor.execute("INSERT INTO fingerprints (account_id, fingerprint_image, fingerprint_name) VALUES (?, ?, ?)", 
               (mary_jones_id, read_image(r'C:\Users\Krupa\Desktop\atm-simulation\fingerprint4.jpeg'), 'Mary Jones Fingerprint 2'))

# Step 7: Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")
