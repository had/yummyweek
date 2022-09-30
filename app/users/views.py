from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, login_required, logout_user

from . import users
from .forms import LoginForm, RegistrationForm
from .models import User
from .. import db


@users.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for("main.index")
            return redirect(next_url)
        flash("Invalid username or credentials")

    return render_template("login.html", login_form=login_form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("main.index"))

@users.route("/register", methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(
            email=registration_form.email.data,
            username=registration_form.nickname.data,
            password=registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration done! Please login")
        return redirect(url_for("users.login"))
    return render_template("register.html", registration_form=registration_form)