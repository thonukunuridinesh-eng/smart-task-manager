from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password_raw = request.form.get('password')

        # 1. Check if the username or email already exists in the database
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already registered. Please try logging in.", "error")
            return redirect(url_for('auth.register'))

        # 2. Hash password and save new user safely
        password = generate_password_hash(password_raw)
        user = User(
            username=username,
            email=email,
            password=password
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash("Registration Successful", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()  # Clear the failed transaction
            flash("An error occurred. Please try again.", "error")
            return redirect(url_for('auth.register'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')

        flash("Invalid Credentials", "error")

    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
