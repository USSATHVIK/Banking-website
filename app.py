from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
import random
import string
import flask_sqlalchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    account_number = db.Column(db.String(12), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    preferred_language = db.Column(db.String(20), default='english')
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        recipient_account = request.form.get('recipient_account')
        amount = float(request.form.get('amount', 0))
        
        recipient = User.query.filter_by(account_number=recipient_account).first()
        
        if not recipient:
            flash('Invalid account number! Please check and try again.', 'error')
        elif recipient.id == current_user.id:
            flash('Cannot transfer money to your own account!', 'error')
        elif amount <= 0:
            flash('Invalid amount!', 'error')
        elif current_user.balance < amount:
            flash('Insufficient balance!', 'error')
        else:
            # Perform the transfer
            current_user.balance -= amount
            recipient.balance += amount
            
            # Record transactions
            sender_transaction = Transaction(
                amount=amount,
                transaction_type='transfer_sent',
                user_id=current_user.id
            )
            recipient_transaction = Transaction(
                amount=amount,
                transaction_type='transfer_received',
                user_id=recipient.id
            )
            
            db.session.add(sender_transaction)
            db.session.add(recipient_transaction)
            db.session.commit()
            
            flash(f'Successfully transferred ₹{amount:.2f} to account: {recipient_account}', 'success')
            return redirect(url_for('dashboard'))
            
    return render_template('transfer.html')

@app.route('/loans')
@login_required
def loans():
    return render_template('loans.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password!', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        preferred_language = request.form.get('language', 'english')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(phone=phone).first():
            flash('Phone number already registered!', 'error')
            return render_template('register.html')
        
        # Generate unique account number
        while True:
            account_number = ''.join(random.choices(string.digits, k=12))
            if not User.query.filter_by(account_number=account_number).first():
                break
        
        new_user = User(
            username=username,
            password=password,
            phone=phone,
            account_number=account_number,
            preferred_language=preferred_language
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Your account number is: ' + account_number, 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/debit', methods=['GET', 'POST'])
@login_required
def debit():
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Invalid amount!', 'error')
        elif amount > current_user.balance:
            flash('Insufficient balance!', 'error')
        else:
            current_user.balance -= amount
            transaction = Transaction(
                amount=amount,
                transaction_type='debit',
                user_id=current_user.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash(f'Successfully debited ₹{amount:.2f}', 'success')
            return redirect(url_for('dashboard'))
    return render_template('debit.html')

@app.route('/credit', methods=['GET', 'POST'])
@login_required
def credit():
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Invalid amount!', 'error')
        else:
            current_user.balance += amount
            transaction = Transaction(
                amount=amount,
                transaction_type='credit',
                user_id=current_user.id
            )
            db.session.add(transaction)
            db.session.commit()
            flash(f'Successfully credited ₹{amount:.2f}', 'success')
            return redirect(url_for('dashboard'))
    return render_template('credit.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    principal = float(request.form.get('principal'))
    rate = float(request.form.get('rate')) / (12 * 100)  # Monthly interest rate
    time = float(request.form.get('time')) * 12  # Time in months
    
    emi = (principal * rate * (1 + rate)**time) / ((1 + rate)**time - 1)
    
    return jsonify({
        'emi': round(emi, 2),
        'total_amount': round(emi * time, 2),
        'interest_amount': round((emi * time) - principal, 2)
    })

if __name__ == '__main__':
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Create a test admin user
        admin = User(
            username='admin',
            password='admin123',
            phone='1234567890',
            account_number='123456789012',
            balance=1000.0,
            preferred_language='english'
        )
        db.session.add(admin)
        db.session.commit()
        
    app.run(host='localhost', port=5000, debug=True)
