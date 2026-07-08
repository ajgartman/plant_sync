from app import app, db, login_manager
from app.forms import LoginForm, RegisterForm, IssueForm, AreaForm,IssueStatusForm
from app.models import User,Issues,Area
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

@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():

    issueStatusForm = IssueStatusForm()
    # Fetching current data
    user_filter = request.args.get("status")

    if user_filter == "open":
        issues = select(Issues).where(Issues.status == "open")
    elif user_filter == "in_progress":
        issues = select(Issues).where(Issues.status == "in_progress")
    elif user_filter == "under_review":
        issues = select(Issues).where(Issues.status == "under_review")
    elif user_filter == "closed":
        issues = select(Issues).where(Issues.status == "closed")
    else:
        issues = select(Issues)

    result = db.session.scalars(issues).all()

    issueStatusForm.status.data = user_filter

    columns = ["ID","Desc.","Date","Submitted By","Completed By","Area","Status","Priority"]


    return render_template("dashboard.html",columns=columns,issues=result,form=issueStatusForm)


@app.route("/add_issue",methods=["GET","POST"])
@login_required
def add_issue():
    form = IssueForm()

    if form.validate_on_submit():
        desc = form.desc.data
        submitted_by = form.submitted_by.data
        completed_by = form.completed_by.data
        area = form.area.data
        status = form.status.data
        priority = form.priority.data

        issue = Issues(desc=desc,
                      submitted_by=submitted_by,
                      completed_by=completed_by,
                      area=area,
                      status=status,
                      priority=priority)

        db.session.add(issue)
        db.session.commit()

        flash("Issue added successfully!",category="success")
        return redirect(url_for("dashboard"))
    return render_template("add_issue.html",form=form)


@app.route("/management",methods=["GET","POST"])
@login_required
def management():

    return render_template("management.html")

@app.route("/add_area",methods=["GET","POST"])
@login_required
def add_area():

    form = AreaForm()

    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data

        area = Area(name=name,
                    desc=desc)

        db.session.add(area)
        db.session.commit()

        flash("Area added successfully!",category="success")
        return redirect(url_for("management"))

    return render_template("add_area.html",form=form)