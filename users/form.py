import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField, DateField, SelectField
from wtforms.validators import Email, DataRequired, ValidationError, equal_to, Length, NumberRange
from flask_wtf import RecaptchaField


def char_check(form, field):
    """
        This function is used to check if the first name and last name contain any special characters
        :param form: form being submitted
        :param field: field being checked
        :return: ValidationError if special character is found
    """
    excluded_characters = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_characters:
            raise ValidationError("This character is not allowed")



def validate_password(self, data_field):
    """
        This function is used to check if the password contains at least 1 lower case, 1 digit, 1 upper case, and 1 special character
        :param data_field: password field being checked
        :return: ValidationError if password does not contain at least 1 lower case, 1 digit, 1 upper case, and 1 special character
    """
    password_chars = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)')
    if not password_chars.match(data_field.data):
        raise ValidationError("Requires at least 1 lower case & 1 digit & 1 upper case & 1 special character")


"""
Classes Developed by Catherine
"""
# Registration form
class RegisterForm(FlaskForm):
    email = EmailField(validators=[Email(), DataRequired()])
    firstname = StringField(validators=[DataRequired(), char_check])
    lastname = StringField(validators=[DataRequired(), char_check])
    password = PasswordField(validators=[DataRequired(), validate_password, Length(min=6, max=12)])
    confirm_password = PasswordField(validators=[equal_to('password', message="Passwords don't match")])
    submit = SubmitField()


# Login form
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()


# Password reset form
class PasswordResetForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()


# Contact form
class ContactForm(FlaskForm):
    entry_num = IntegerField()
    message = StringField()
    submit = SubmitField()


"""
Forms developed by Harsh
"""
# Exercise log form
class ExerciseLogForm(FlaskForm):
    exercise_type = SelectField('Type of Exercise', choices=[
        ('running', 'Running'),
        ('swimming', 'Swimming'),
        ('cycling', 'Cycling'),
        # Add more types of exercise here...
    ], validators=[DataRequired()])

    entry_num = IntegerField('Entry')
    duration = IntegerField('Duration (minutes)', validators=[
        DataRequired(),
        NumberRange(min=1)  # Duration must be at least 1 minute
    ])

    intensity = SelectField('Intensity', choices=[
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('intense', 'Intense'),
        # Add more levels of intensity here...
    ], validators=[DataRequired()])
    exercise_date = DateField('Exercise Date', format='%Y-%m-%d', validators=[DataRequired()])
    comments = StringField(validators=[DataRequired()])

    submit = SubmitField()


# Delete account form
class DeleteAccountForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()
