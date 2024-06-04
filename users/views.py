import bcrypt
from app import db
from flask import Blueprint, render_template, flash, redirect, url_for
from users.form import RegisterForm, LoginForm, PasswordResetForm, ContactForm, DeleteAccountForm
from flask_login import login_user, login_required, logout_user, current_user
from models import User, contact_form, Co2Values

# Sets blueprint folder
users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Developed by Harsh
        This function is used to register a new user
        :return: renders the register page
    """
    # Registration form
    form = RegisterForm()

    # If request method is POST or form is valid
    if form.validate_on_submit():

        # Checks if email already exists in database
        user = User.query.filter_by(email=form.email.data).first()

        # If email exists redirects user to signup page
        if user:
            flash('Email address already exists')
            return render_template('users/Register.html', form=form)

        # Create new user
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data,
                        role='user')

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Create their carbon emissions
        new_calculation = Co2Values(
                id=new_user.id,
                email=new_user.email,
                transportval=0,
                foodval=0,
                electricalval=0,
                finalval=0
            )
        db.session.add(new_calculation)
        db.session.commit()
        # Sends user to login page
        return redirect(url_for('users.login'))

    return render_template('users/Register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Developed by Harsh
        This function is used to login a user
        :return: renders the login page
    """
    # Login form
    form = LoginForm()

    # Checks the login information being submitted
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            flash('Invalid credentials')
            return render_template('users/Login.html', form=form)

        else:
            login_user(user)


            return redirect(url_for('users.account'))

    return render_template('users/Login.html', form=form)



@users_blueprint.route('/passwordreset', methods=['GET', 'POST'])
def password_reset():
    """
        This function is used to reset a users password
        :return: renders the password reset page
    """
    # Password reset form
    form = PasswordResetForm()

    return render_template('users/PasswordResetForm.html', form=form)


@users_blueprint.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Developed by Harsh
        This function is used to contact the admin
        :return: renders the contact page
    """

    # displays contact form
    form = ContactForm()
    # Checks if form is submitted
    if form.is_submitted():
        # Creates new submission
        new_submission = contact_form(
            entry_num=form.entry_num.data,
            message=form.message.data)
        # Adds new submission to database
        db.session.add(new_submission)
        # Commits changes to database
        db.session.commit()
        # Redirects user to contact page
        flash('Your message has been submitted!')
        return redirect(url_for('users.contact'))

    return render_template('users/Contact.html', form=form)


"""
    This function is used to view a users account
    :return: renders the account page
"""


@users_blueprint.route('/account')
@login_required
def account():
    """
    Developed by Catherine
        This function is used to edit a users account
        :return: renders the edit account page
    """
    return render_template('users/Account.html',
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           email=current_user.email)





@users_blueprint.route('/deleteaccount', methods=['GET', 'POST'])
@login_required
def delete_account():
    """
    Developed by Catherine
        This function is used to edit a users account
        :return: renders the edit account page
    """
    # Delete account form
    form = DeleteAccountForm()
    # Checks user info so that only the correct user is deleted
    user = User.query.filter_by(email=form.email.data).first()
    # Checks the data being submitted matches the users info
    if form.validate_on_submit():
        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            flash('Invalid credentials')
            return render_template('users/DeleteAccount.html', form=form)
        else:
            # Delete & log out the current user
            db.session.delete(current_user)
            logout_user()
            db.session.commit()
            return redirect(url_for('main'))

    return render_template('users/DeleteAccount.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    """
    Developed by Harsh
        This function is used to logout a user
        :return: redirects to the main page
    """
    # Logs out current user
    logout_user()
    return redirect(url_for('main'))



@users_blueprint.route("/ViewMessages", methods=['GET', 'POST'])
def view_messages():
    """
    Developed by Harsh
        This function is used to view messages
        :return: renders the view messages page
    """
    messages = contact_form.query.all()
    if not messages:
        flash('There are no messages to view')
        return render_template("users/Account.html")
    else:
        return render_template("users/ViewMessages.html", name=current_user.firstname, messages=messages)
