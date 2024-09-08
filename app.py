from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Initialize web3
# Use web3.js in the frontend for interacting with the blockchain

@app.route('/')
def index():
    # return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wallet_address = request.form['wallet_address']
        password = request.form['password']
        user = User.query.filter_by(wallet_address=wallet_address, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        wallet_address = request.form['wallet_address']
        password = request.form['password']
        new_user = User(wallet_address=wallet_address, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            msg = "user already exists!"
            return render_template('register.html',message=msg)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        goal = int(request.form['goal'])
        # Interact with the contract to create a project using web3.js in the frontend
        return redirect(url_for('dashboard'))
    return render_template('create_project.html')

@app.route('/view_projects')
def view_projects():
    # Fetch projects from the contract using web3.js in the frontend
    return render_template('view_projects.html')

@app.route('/my_projects')
def my_projects():
    # Fetch user's projects from the contract using web3.js in the frontend
    return render_template('my_projects.html')

@app.route('/donate/<int:project_id>')
def donate(project_id):
    return render_template('donate.html', project_id=project_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
