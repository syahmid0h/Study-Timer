from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from .models import User
from .extensions import db, bcrypt, login_manager
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

auth = Blueprint('auth', __name__)

# This is our .form nihal -_- -syahmi

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('This username has already been taken. Please choose another one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Change Password")

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.new_password.data:
            raise ValidationError('Passwords do not match.')
   

@auth.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account successfully created! You can now log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        print("Form submitted and validated.")  # Debugging output
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            print("User not found.")  
        else:
            print(f"User found: {user.username}")

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print(f"User {user.username} logged in.")  
            return redirect(url_for('views.index'))
        else:
            print("Password check failed.")  
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        print("Form validation failed.")  
        print(form.errors)  
    return render_template('login.html', form=form)


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Current password is incorrect', 'danger')
    return render_template('account.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if current_user.is_authenticated:
            logout_user()  # Log the user out
            flash('You have been logged out.', 'info')
            return redirect(url_for('auth.login'))  # Redirect to login after logging out
        else:
            flash('You are not logged in.', 'warning')  # Flash message for unauthorized access
            return redirect(url_for('views.index'))  # Redirect to index

    # Handle GET request by rendering the logout confirmation page
    return render_template('logout.html')  # Render logout confirmation page