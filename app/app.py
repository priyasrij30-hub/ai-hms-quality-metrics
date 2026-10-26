from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Keep the demo prediction feature isolated from the core HMS routes.
from risk_prediction import risk_bp
app.register_blueprint(risk_bp)

# Database initialization
def init_db():
    conn = sqlite3.connect('quickmed.db')
    cursor = conn.cursor()

    # Create the patients table
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        dob DATE NOT NULL,
                        contact TEXT NOT NULL,
                        medical_history TEXT)''')

    # Create the appointments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        date DATE NOT NULL,
                        time TIME NOT NULL,
                        FOREIGN KEY (patient_id) REFERENCES patients(id))''')

    # Create the staff table
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        role TEXT NOT NULL)''')

    # Users table for authentication
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''CREATE TABLE users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     firstname TEXT NOT NULL,
                     lastname TEXT NOT NULL,
                     email TEXT UNIQUE NOT NULL,
                     number TEXT NOT NULL,
                     password TEXT NOT NULL)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

# Routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = sqlite3.connect('quickmed.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                '''INSERT INTO users (firstname, lastname, email, number, password) 
                VALUES (?, ?, ?, ?, ?)''',
                (firstname, lastname, email, number, hashed_password)
            )
            conn.commit()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists. Please use a different email.", "danger")
        finally:
            conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Email and Password are required.", "danger")
            return render_template('login.html')

        conn = sqlite3.connect('quickmed.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[5], password):  # user[5] is the hashed password
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/register-patient', methods=['GET', 'POST'])
def register_patient():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        contact = request.form['contact']
        medical_history = request.form['medical-history']

        conn = sqlite3.connect('quickmed.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, dob, contact, medical_history) VALUES (?, ?, ?, ?)",
                       (name, dob, contact, medical_history))
        conn.commit()
        conn.close()

        flash('Patient registered successfully!', 'success')
        return redirect(url_for('patient_list'))

    return render_template('patient-registration.html')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient_id = request.form['patient-id']
        date = request.form['date']
        time = request.form['time']

        conn = sqlite3.connect('quickmed.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (patient_id, date, time) VALUES (?, ?, ?)",
                       (patient_id, date, time))
        conn.commit()
        conn.close()

        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('appointments'))

    return render_template('appointments.html')

@app.route('/patient-list')
def patient_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('quickmed.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()

    return render_template('patient-list.html', patients=patients)

@app.route('/staff-management', methods=['GET', 'POST'])
def staff_management():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['staff-name']
        role = request.form['role']

        conn = sqlite3.connect('quickmed.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO staff (name, role) VALUES (?, ?)", (name, role))
        conn.commit()
        conn.close()

        flash('Staff member added successfully!', 'success')
        return redirect(url_for('staff_management'))

    return render_template('staff-management.html')

@app.route('/view-appointments')
def view_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('quickmed.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT a.id, p.name, a.date, a.time FROM appointments a
                      JOIN patients p ON a.patient_id = p.id''')
    appointments = cursor.fetchall()
    conn.close()

    return render_template('view-appointments.html', appointments=appointments)

@app.route('/view-staff')
def view_staff():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('quickmed.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM staff')
    staff = cursor.fetchall()
    conn.close()

    return render_template('view-staff.html', staff=staff)

# Updated code for production
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

