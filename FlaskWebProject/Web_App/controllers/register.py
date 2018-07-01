from flask import render_template, Blueprint, request, session, flash
from Web_App.models import UserAccount, db
from Web_App.forms import RegisterForm
from passlib.hash import sha256_crypt

registerAccount_blueprint = Blueprint(
    'registerAccount',
    __name__,
    template_folder='../templates/main',
    url_prefix="/register")

# User Register
@registerAccount_blueprint.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        firstName = form.firstName.data
        surName = form.surName.data
        email = form.email.data
        phone = form.phone.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Add account
        newAccount = UserAccount(title=title,firstName=firstName,surName=surName,email=email,phone=phone,username=username,password=password)
        db.session.add(newAccount)

        # Commit to DB
        db.session.commit()

        # Close connection
        db.session.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
