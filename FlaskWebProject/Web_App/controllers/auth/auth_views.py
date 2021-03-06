from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
from Web_App.controllers.auth import auth_blueprint
from functools import wraps
from Web_App.models import UserAccount
##from ..email import send_email
from Web_App.forms import LoginForm, ChangePasswordForm, RegisterForm #,RegistrationForm,PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
import pdb ##pdb.set_trace() #debug mode
from Web_App import db
from Web_App.controllers.extension.mail import send_email

@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.blueprint != 'main' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('main/auth/unconfirmed.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        POST_USERNAME = form.username.data
        POST_PASSWORD = form.password.data
        user = UserAccount.query.filter_by(username=POST_USERNAME).first()
        if user is not None:
            if user.password is not None and user.verify_password(POST_PASSWORD):
                login_user(user, form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                flash('You are now logged in', 'success')
                return redirect(next)
            else:
                flash('Invalid password')
        else:
            flash('Username not found')
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
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

# User Register
@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = sha256_crypt.encrypt(str(form.password.data))
        # Add account
        newAccount = UserAccount(title=form.title.data,firstName=form.firstName.data,surName=form.surName.data,email=form.email.data,phone=form.phone.data,username=form.username.data,password=password)
        db.session.add(newAccount)

        ## Commit to DB
        db.session.commit()

        ## Close connection
        #db.session.close()
        
        #Generate and send confirmation token
        token = newAccount.generate_confirmation_token()
        send_email(newAccount.email, 'Confirm Your Account','main/mail/confirmAccount', user=newAccount, token=token)
        flash('A confirmation email has been sent to you, please click on the link to approve your subscription')

        return redirect(url_for('auth.login'))
    elif form.is_submitted():
        error = 'Information incorrect, please check all fields and submit again'
        flash(form.errors)
        return render_template('main/register.html',form=form, error=error)
    return render_template('main/register.html', form=form)

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


@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'error')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'main/mail/confirmAccount', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.', 'success')
    return redirect(url_for('main.index'))


@auth_blueprint.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = sha256_crypt.encrypt(str(form.password.data))
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.','error')
    return render_template("main/auth/change_password.html", form=form)


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

#@auth_blueprint.route('/change-password', methods=['GET', 'POST'])
#@is_logged_in
#def change_password():
#    form = ChangePasswordForm()
#    if request.method == 'POST' and form.validate():
#        if UserAccount.verify_password(form.old_password.data):
#            UserAccount.password = form.password.data
#            #db.session.add(current_user)
#            #db.session.commit()
#            flash('Your password has been updated.')
#            return redirect(url_for('main.index'))
#        else:
#            flash('Invalid password.')
#    return render_template("auth/change_password.html", form=form)

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