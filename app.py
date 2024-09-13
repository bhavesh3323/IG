from flask import Flask, request, redirect, render_template
import sqlite3

app = Flask(__name__)

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

    return redirect('/')  # Redirect back to home or another page

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Start the Flask app
    app.run(debug=True)
