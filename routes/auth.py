from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if db.session.query(User).filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return redirect(url_for("auth.register"))
        user = User(name=name, email=email, password_hash=generate_password_hash(password))
        db.session.add(user); db.session.commit()
        # seed default categories
        for cat in ["Salary", "Food", "Rent", "Transport", "Utilities", "Entertainment", "Shopping", "Other"]:
            db.session.add(Category(user_id=user.id, name=cat))
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard.home"))
        flash("Invalid credentials.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
