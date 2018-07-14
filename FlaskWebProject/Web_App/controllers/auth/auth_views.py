from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
from Web_App.controllers.auth import auth_blueprint
from functools import wraps
from Web_App.models import UserAccount
##from ..email import send_email
from Web_App.forms import LoginForm, ChangePasswordForm #,RegistrationForm,PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
#import pdb ##pdb.set_trace() #debug mode

#@auth.before_app_request
#def before_request():
#    if current_user.is_authenticated:
#        current_user.ping()
#        if not current_user.confirmed \
#                and request.endpoint \
#                and request.blueprint != 'auth' \
#                and request.endpoint != 'static':
#            return redirect(url_for('auth.unconfirmed'))


#@auth.route('/unconfirmed')
#def unconfirmed():
#    if current_user.is_anonymous or current_user.confirmed:
#        return redirect(url_for('main.index'))
#    return render_template('auth/unconfirmed.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        POST_USERNAME = form.username.data
        POST_PASSWORD = form.password.data
        user = UserAccount.query.filter_by(username=POST_USERNAME).first()
        if user is not None:
            if user.password is not None and user.verify_password(POST_PASSWORD):
                #session['logged_in'] = True
                #session['username'] = POST_USERNAME
                login_user(user)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('call.CoveredCallsResults')
                flash('You are now logged in', 'success')
                return redirect(next)
            else:
                error = 'Invalid password'
                return render_template('main/auth/login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    #flash(form.errors)@is_logged_in
    return render_template('main/auth/login.html', form=form)

# Check if user logged in
#def is_logged_in(f):
#    @wraps(f)
#    def wrap(*args, **kwargs):
#        if 'logged_in' in session:
#            return f(*args, **kwargs)
#        else:
#            flash('Unauthorized, Please login', 'danger')
#            return redirect(url_for('auth.login'))
#    return wrap

@auth_blueprint.route('/logout')
@login_required
def logout():
    #session.clear()
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


#@auth.route('/register', methods=['GET', 'POST'])
#def register():
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        user = User(email=form.email.data,
#                    username=form.username.data,
#                    password=form.password.data)
#        db.session.add(user)
#        db.session.commit()
#        token = user.generate_confirmation_token()
#        send_email(user.email, 'Confirm Your Account',
#                   'auth/email/confirm', user=user, token=token)
#        flash('A confirmation email has been sent to you by email.')
#        return redirect(url_for('auth.login'))
#    return render_template('auth/register.html', form=form)


#@auth.route('/confirm/<token>')
#@login_required
#def confirm(token):
#    if current_user.confirmed:
#        return redirect(url_for('main.index'))
#    if current_user.confirm(token):
#        db.session.commit()
#        flash('You have confirmed your account. Thanks!')
#    else:
#        flash('The confirmation link is invalid or has expired.')
#    return redirect(url_for('main.index'))


#@auth.route('/confirm')
#@login_required
#def resend_confirmation():
#    token = current_user.generate_confirmation_token()
#    send_email(current_user.email, 'Confirm Your Account',
#               'auth/email/confirm', user=current_user, token=token)
#    flash('A new confirmation email has been sent to you by email.')
#    return redirect(url_for('main.index'))


#@auth.route('/change-password', methods=['GET', 'POST'])
#@login_required
#def change_password():
#    form = ChangePasswordForm()
#    if form.validate_on_submit():
#        if current_user.verify_password(form.old_password.data):
#            current_user.password = form.password.data
#            db.session.add(current_user)
#            db.session.commit()
#            flash('Your password has been updated.')
#            return redirect(url_for('main.index'))
#        else:
#            flash('Invalid password.')
#    return render_template("auth/change_password.html", form=form)


#@auth.route('/reset', methods=['GET', 'POST'])
#def password_reset_request():
#    if not current_user.is_anonymous:
#        return redirect(url_for('main.index'))
#    form = PasswordResetRequestForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(email=form.email.data).first()
#        if user:
#            token = user.generate_reset_token()
#            send_email(user.email, 'Reset Your Password',
#                       'auth/email/reset_password',
#                       user=user, token=token,
#                       next=request.args.get('next'))
#        flash('An email with instructions to reset your password has been '
#              'sent to you.')
#        return redirect(url_for('auth.login'))
#    return render_template('auth/reset_password.html', form=form)


#@auth.route('/reset/<token>', methods=['GET', 'POST'])
#def password_reset(token):
#    if not current_user.is_anonymous:
#        return redirect(url_for('main.index'))
#    form = PasswordResetForm()
#    if form.validate_on_submit():
#        if User.reset_password(token, form.password.data):
#            db.session.commit()
#            flash('Your password has been updated.')
#            return redirect(url_for('auth.login'))
#        else:
#            return redirect(url_for('main.index'))
#    return render_template('auth/reset_password.html', form=form)


#@auth.route('/change_email', methods=['GET', 'POST'])
#@login_required
#def change_email_request():
#    form = ChangeEmailForm()
#    if form.validate_on_submit():
#        if current_user.verify_password(form.password.data):
#            new_email = form.email.data
#            token = current_user.generate_email_change_token(new_email)
#            send_email(new_email, 'Confirm your email address',
#                       'auth/email/change_email',
#                       user=current_user, token=token)
#            flash('An email with instructions to confirm your new email '
#                  'address has been sent to you.')
#            return redirect(url_for('main.index'))
#        else:
#            flash('Invalid email or password.')
#    return render_template("auth/change_email.html", form=form)


#@auth.route('/change_email/<token>')
#@login_required
#def change_email(token):
#    if current_user.change_email(token):
#        db.session.commit()
#        flash('Your email address has been updated.')
#    else:
#        flash('Invalid request.')
#    return redirect(url_for('main.index'))