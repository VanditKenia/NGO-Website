from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="k1ng@k1ng",
            database="mumbai_ngos"
        )
        self.cursor = self.conn.cursor()

    def check_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        return self.cursor.fetchone() is not None

    def add_volunteer(self, name, email, contact):
        self.cursor.execute("INSERT INTO volunteers (name, email, contact) VALUES (%s, %s, %s)", (name, email, contact))
        self.conn.commit()

    def add_ngo(self, name, ngo_id, location, contact):
        self.cursor.execute("INSERT INTO ngos (name, ngo_id, location, contact) VALUES (%s, %s, %s, %s)", (name, ngo_id, location, contact))
        self.conn.commit()

    def get_ngos(self):
        self.cursor.execute("SELECT * FROM ngos")
        return self.cursor.fetchall()

    def add_event(self, name, details, location, date_time, ngo_name):
        self.cursor.execute("INSERT INTO events (name, details, location, date_time, ngo_name) VALUES (%s, %s, %s, %s, %s)", (name, details, location, date_time, ngo_name))
        self.conn.commit()

    def get_events(self):
        self.cursor.execute("SELECT * FROM events")
        return self.cursor.fetchall()

db = Database()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.check_login(username, password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/volunteer_form', methods=['GET', 'POST'])
def volunteer_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        db.add_volunteer(name, email, contact)
        return redirect(url_for('dashboard'))
    return render_template('volunteer_form.html')

@app.route('/ngo_details', methods=['GET', 'POST'])
def ngo_details():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        ngo_id = request.form['ngo_id']
        location = request.form['location']
        contact = request.form['contact']
        db.add_ngo(name, ngo_id, location, contact)
    ngos = db.get_ngos()
    return render_template('ngo_details.html', ngos=ngos)

@app.route('/event_details', methods=['GET', 'POST'])
def event_details():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']
        location = request.form['location']
        date_time = request.form['date_time']
        ngo_name = request.form['ngo_name']
        db.add_event(name, details, location, date_time, ngo_name)
    events = db.get_events()
    return render_template('event_details.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)