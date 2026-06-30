from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,FloatField,SelectField
from wtforms.validators import DataRequired, EqualTo, number_range


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    account_choices = [("contractor","Contractor"),("plant_management","Plant Management"),("admin","Admin")]
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    account_type = SelectField("Please select user type",choices=account_choices)
    submit = SubmitField("Login")

