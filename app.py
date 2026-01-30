from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import firebase_admin
from firebase_admin import credentials, auth
import random
import secrets

# Initialize the Firebase Admin SDK with your service account key (adjust the path accordingly)
cred = credentials.Certificate(r"C:\Users\manir\OneDrive\Desktop\atm-simulation\firebase-service-account.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to check if the fingerprint matches any in the database
def verify_fingerprint(account_id, fingerprint_image):
    conn = get_db_connection()
    fingerprints = conn.execute('SELECT fingerprint_image FROM fingerprints WHERE account_id = ?', 
                                (account_id,)).fetchall()
    conn.close()
    
    # Check if the provided fingerprint matches any stored fingerprints
    for fingerprint in fingerprints:
        if fingerprint['fingerprint_image'] == fingerprint_image:
            return True
    return False

@app.route('/')
def front_page():
    return render_template('front_page.html')

@app.route('/validate', methods=['POST'])
def validate():
    account_number = request.form['account_number']
    cvv = request.form['cvv']
    expiry_date = request.form['expiry_date']

    conn = get_db_connection()
    account = conn.execute('SELECT * FROM accounts WHERE account_number = ?', 
                            (account_number,)).fetchone()
    conn.close()

    if account:
        # Check if CVV and expiry date are correct
        if account['cvv'] == cvv and account['expiry_date'] == expiry_date:
            # Store the account number in the session
            session['account_number'] = account_number
            return render_template('transaction.html', name=account['name'], account_number=account_number)
        else:
            flash("Invalid CVV or expiry date.", "error")  # Flash error message
            return render_template('indexer.html')
    else:
        flash("No user exists with the entered account number.", "error")  # Flash error message
        return render_template('indexer.html')


# OTP page, simplified
@app.route('/dummy_otp', methods=['GET', 'POST'])
def dummy_otp():
    # We assume that the session stores the account number
    account_number = session.get('account_number')

    if not account_number:
        flash("Session expired. Please start again.")
        return redirect(url_for('front_page'))

    conn = get_db_connection()
    account = conn.execute('SELECT phone_number FROM accounts WHERE account_number = ?', 
                           (account_number,)).fetchone()
    conn.close()

    if request.method == 'POST':
        otp_input = (
            request.form.get('otp1', '') +
            request.form.get('otp2', '') +
            request.form.get('otp3', '') +
            request.form.get('otp4', '') +
            request.form.get('otp5', '') +
            request.form.get('otp6', '')
        )

        # Here you would integrate Firebase OTP verification
        # Assuming the OTP verification is successful
        if otp_input == "123456":  # Dummy OTP for testing
            return redirect(url_for('success'))
        else:
            return redirect(url_for('unsuccess'))
    
    return render_template('dummy_otp.html', phone_number=account['phone_number'])

@app.route('/process_transaction', methods=['POST'])
def process_transaction():
    account_number = request.form.get('account_number')
    amount = request.form.get('amount')
    password = request.form.get('password')
    fingerprint_file = request.files.get('fingerprint')

    if not fingerprint_file:
        return "No fingerprint file uploaded", 400

    fingerprint_image = fingerprint_file.read()

    conn = get_db_connection()
    account = conn.execute('SELECT * FROM accounts WHERE account_number = ? AND password = ?', 
                            (account_number, password)).fetchone()

    if account:
        account_id = account['id']
        
        # Verify the fingerprint
        if verify_fingerprint(account_id, fingerprint_image):
            # Store account number in the session for later use in the OTP process
            session['account_number'] = account_number
            # Proceed to dummy_otp page after transaction
            return redirect(url_for('dummy_otp'))
        else:
            flash('Fingerprint mismatch. Proceeding to OTP page anyway.')
            session['account_number'] = account_number
            return redirect(url_for('dummy_otp'))
    else:
        flash('Invalid account details. Proceeding to OTP page anyway.')
        session['account_number'] = account_number
        return redirect(url_for('dummy_otp'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/unsuccess')
def unsuccess():
    return render_template('unsuccess.html')

@app.route('/remove_money', methods=['GET', 'POST'])
def remove_money():
    message = None
    if request.method == 'POST':
        account_number = request.form['account_number']
        cvv = request.form['cvv']
        expiry_date = request.form['expiry_date']

        conn = get_db_connection()
        account = conn.execute('SELECT * FROM accounts WHERE account_number = ? AND cvv = ? AND expiry_date = ?', 
                                (account_number, cvv, expiry_date)).fetchone()
        conn.close()

        if account:
            # Account is valid; proceed with the next steps
            return redirect(url_for('transaction', name=account['name'], account_number=account_number))
        else:
            # No valid account found
            message = "No user exists with the provided details."
    
    return render_template('indexer.html', message=message)

@app.route('/add_money', methods=['GET', 'POST'])
def add_money():
    message = None
    if request.method == 'POST':
        account_number = request.form['account_number']
        cvv = request.form['cvv']
        expiry_date = request.form['expiry_date']

        conn = get_db_connection()
        account = conn.execute('SELECT * FROM accounts WHERE account_number = ? AND cvv = ? AND expiry_date = ?', 
                                (account_number, cvv, expiry_date)).fetchone()
        conn.close()

        if account:
            # Account is valid; proceed with the next steps
            return redirect(url_for('transaction', name=account['name'], account_number=account_number))
        else:
            # No valid account found
            message = "No user exists with the provided details."
    
    return render_template('adder.html', message=message)



if __name__ == '__main__':
    app.run(debug=True)

