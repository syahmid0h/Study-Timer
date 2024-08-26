from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')

def login():                #Login text, 3 of these is the defined routes
    return "<p>Login</p>"   #<p></p> Is the paragraph HTML 

@auth.route('/logout')      #Logout text, auth.route is for the url to go to the "Login", "Logout", "Signup" page when the end of the url has /logout, /login, /sign-up ykwim :)
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up')     #Sign up text
def sign_up():
    return "<p>Sign Up</p>"