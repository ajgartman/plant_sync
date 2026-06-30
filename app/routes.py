from app import app, db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask import flash, url_for, redirect, render_template,request
from sqlalchemy import select,func
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        query = select(User).where(User.username == form.username.data)
        user = db.session.scalars(query).one_or_none()
        if user and check_password_hash(user.pw_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        flash("Login failed!", "danger")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, pw_hash=generate_password_hash(form.password.data),account_type=form.account_type.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Registered and logged in successfully!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/dashboard")
@login_required
def dashboard():

    columns = ["ID","Desc.","Date","Submitted By","Completed By","Area","Status","Priority"]


    return render_template("dashboard.html",columns=columns)