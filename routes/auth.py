from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from database.database import db
from database.models import User, GoogleAdsAccount

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        company_name = request.form.get('company_name', 'ABC Electronics')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered.', 'warning')
            return render_template('auth/register.html')

        new_user = User(email=email, full_name=full_name, company_name=company_name, is_demo_mode=True)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Create default Demo Account for user
        demo_account = GoogleAdsAccount(
            user_id=new_user.id,
            customer_id='892-410-9921',
            account_name=f'{company_name} Google Ads Account',
            is_connected=True,
            connection_type='DEMO'
        )
        db.session.add(demo_account)
        db.session.commit()

        login_user(new_user)
        flash('Registration successful! Demo mode activated for your Google Ads account.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        company_name = request.form.get('company_name')
        new_password = request.form.get('new_password')

        current_user.full_name = full_name
        current_user.company_name = company_name

        if new_password and len(new_password) >= 6:
            current_user.set_password(new_password)
            flash('Password updated successfully.', 'success')

        db.session.commit()
        flash('Profile settings saved.', 'success')

    return render_template('auth/profile.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        flash(f'If an account exists for {email}, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')
