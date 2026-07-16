from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,FloatField,SelectField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, EqualTo, number_range, Optional


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

class IssueForm(FlaskForm):
    status_selection = [("open","Open"),("in_progress","In Progress"),("under_review","Under Review"),("closed","Closed")]
    priority_selection = [("low","Low"),("medium","Medium"),("high","High"),("critical","Critical")]
    desc = TextAreaField("Please provide description of the issue: ",validators=[DataRequired()])
    # date = DateField("Raised on: ",format="%Y-%m-%d",validators=[DataRequired()])
    # submitted_by = IntegerField("Submitted By: ",validators=[DataRequired()])
    completed_by = IntegerField("Completed By",validators=[])
    area = IntegerField("ID of the area",validators=[DataRequired()])
    status = SelectField("Current status of the issue",choices=status_selection,validators=[DataRequired()])
    priority = SelectField("Priority of the Issue",validators=[DataRequired()],choices=priority_selection)
    submit = SubmitField("Add")


class AreaForm(FlaskForm):
    name = StringField("Area Name",validators=[DataRequired()])
    desc = TextAreaField("Area description", validators=[DataRequired()])
    submit = SubmitField("Add")


class IssueStatusForm(FlaskForm):
    status_selection = [("all","All"),("open", "Open"), ("in_progress", "In Progress"), ("under_review", "Under Review"),
                        ("closed", "Closed")]
    status = SelectField("Filter by status:", choices=status_selection, validators=[DataRequired()])