from flask import render_template, session, request, Blueprint, send_from_directory, flash, url_for, request
from passlib.hash import sha256_crypt
from functools import wraps
from Web_App.models import UserAccount, db

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/main')

# User login
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        POST_USERNAME = request.form['username']
        POST_PASSWORD = request.form['password']

        # Get user by username
        query = UserAccount.query.filter_by(username=POST_USERNAME).first()

        if query and query.UserID > 0:
            # Get stored hash
            password = query.password

            # Compare Passwords
            if sha256_crypt.verify(POST_PASSWORD, password):
                # Passed
                session['logged_in'] = True
                session['username'] = POST_USERNAME

                flash('You are now logged in', 'success')
                return redirect(url_for('call.CoveredCallsResults'))
            else:
                error = 'Invalid password'
                return render_template('login.html', error=error)
            # Close connection
            db.session.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('auth.login'))
    return wrap

# Logout
@auth_blueprint.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out. Thanks for using CoveredCalls application', 'success')
    return redirect(url_for('auth.login'))
