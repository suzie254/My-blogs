from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from ..models import User

@auth.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        user_save_id = user.save()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form = form)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()

        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember.data)
            
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')
        
    return render_template('auth/login.html', form = login_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))