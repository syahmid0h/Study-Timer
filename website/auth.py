from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/login')
def login():
    return render_template('login 2.html')

@auth.route('/account')
def account():
    return render_template('account.html')