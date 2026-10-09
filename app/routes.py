from app import app, db, login_manager
from app.forms import LoginForm, RegisterForm, IssueForm, AreaForm, IssueStatusForm, UpdateIssueForm
from app.models import User,Issues,Area
from flask import abort, flash, url_for, redirect, render_template, request
from sqlalchemy import func, select
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user


MANAGEMENT_ROLES = {"plant_management", "admin"}


def management_required():
    if current_user.account_type not in MANAGEMENT_ROLES:
        abort(403)


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
        existing_user = db.session.scalar(select(User).where(User.username == form.username.data))
        if existing_user:
            flash("That username is already taken.", "danger")
        else:
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
    status_counts = dict(
        db.session.execute(select(Issues.status, func.count(Issues.id)).group_by(Issues.status)).all())
    issue_count = sum(status_counts.values())
    open_count = status_counts.get("open", 0)
    active_count = status_counts.get("in_progress", 0) + status_counts.get("under_review", 0)
    critical_count = db.session.scalar(
        select(func.count(Issues.id)).where(
            Issues.priority == "critical", Issues.status != "closed")) or 0
    area_count = db.session.scalar(select(func.count(Area.id))) or 0
    recent_issues = db.session.scalars(
        select(Issues).order_by(Issues.date.desc(), Issues.id.desc()).limit(5)).all()

    return render_template(
        "index.html",
        issue_count=issue_count,
        open_count=open_count,
        active_count=active_count,
        critical_count=critical_count,
        area_count=area_count,
        recent_issues=recent_issues,
        status_counts=status_counts,
        now_hour=datetime.now().hour,
    )

@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    issue_status_form = IssueStatusForm()
    user_filter = request.args.get("status", "all")
    allowed_statuses = {choice[0] for choice in issue_status_form.status.choices}
    if user_filter not in allowed_statuses:
        user_filter = "all"

    issues = select(Issues)
    if user_filter != "all":
        issues = issues.where(Issues.status == user_filter)

    result = db.session.scalars(issues.order_by(Issues.date.desc(), Issues.id.desc())).all()
    issue_status_form.status.data = user_filter

    columns = ["ID", "Desc.", "Date", "Submitted By", "Completed By", "Area", "Status", "Priority", "Details"]
    return render_template(
        "dashboard.html",
        columns=columns,
        issues=result,
        form=issue_status_form,
        can_manage=current_user.account_type in MANAGEMENT_ROLES)


@app.route("/add_issue",methods=["GET","POST"])
@login_required
def add_issue():
    form = IssueForm()
    form.area.choices = [(area.id, area.name) for area in db.session.scalars(select(Area).order_by(Area.name)).all()]

    if form.validate_on_submit():
        desc = form.desc.data
        area = db.session.get(Area, form.area.data)
        if area is None:
            form.area.errors.append("Please choose an existing plant area.")
            return render_template("add_issue.html", form=form)

        completed_by = form.completed_by.data.strip() or None
        status = form.status.data
        priority = form.priority.data

        issue = Issues(desc=desc,
                      submitted_by_id=current_user.id,
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
    management_required()
    return render_template("management.html")

@app.route("/add_area",methods=["GET","POST"])
@login_required
def add_area():
    management_required()
    form = AreaForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        desc = form.desc.data.strip()
        if not name or not desc:
            if not name:
                form.name.errors.append("Enter an area name.")
            if not desc:
                form.desc.errors.append("Enter an area description.")
            return render_template("add_area.html", form=form)

        area = Area(name=name,
                    desc=desc)

        db.session.add(area)
        db.session.commit()

        flash("Area added successfully!",category="success")
        return redirect(url_for("management"))

    return render_template("add_area.html",form=form)


@app.route("/inspect_issue/<int:issue_id>", methods=["GET"])
@login_required
def inspect_issue(issue_id):
    issue = db.session.get(Issues, issue_id)
    if issue is None:
        abort(404)
    form = UpdateIssueForm(obj=issue)
    can_manage = current_user.account_type in MANAGEMENT_ROLES
    return render_template("inspect_issue.html", issue=issue, form=form, can_manage=can_manage)


@app.route("/issues/<int:issue_id>/update", methods=["POST"])
@login_required
def update_issue(issue_id):
    management_required()
    issue = db.session.get(Issues, issue_id)
    if issue is None:
        abort(404)

    form = UpdateIssueForm()
    if form.validate_on_submit():
        issue.status = form.status.data
        issue.completed_by = form.completed_by.data.strip() or None
        db.session.commit()
        flash("Issue updated.", "success")
    else:
        flash("Please choose a valid status.", "danger")

    return redirect(url_for("inspect_issue", issue_id=issue.id))
