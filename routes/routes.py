from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models import User, Transaction, Category

app_routes = Blueprint("app_routes", __name__)

@app_routes.route("/")
def home():
    return redirect(url_for("app_routes.login"))

# ------------------ Auth ------------------
@app_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("app_routes.register"))

        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for("app_routes.login"))

    return render_template("register.html")

@app_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("app_routes.dashboard"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")

@app_routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("app_routes.login"))

# ------------------ Dashboard ------------------
@app_routes.route("/dashboard")
@login_required
def dashboard():
    transactions = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.id.desc())
        .all()
    )

    income = sum(t.amount for t in transactions if t.type == "income")
    expenses = sum(t.amount for t in transactions if t.type == "expense")
    balance = income - expenses

    return render_template(
        "dashboard.html",
        transactions=transactions,
        income=income,
        expenses=expenses,
        balance=balance,
    )

# ------------------ Add Transaction ------------------
@app.route("/add_transaction", methods=["GET", "POST"])
@login_required
def add_transaction():
    categories = Category.query.all()  # Load categories for dropdown

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            txn_type = request.form.get("type")  # "income" or "expense"
            description = request.form.get("description")
            category_id = int(request.form.get("category_id"))

            new_txn = Transaction(
                amount=amount,
                type=txn_type,
                description=description,
                user_id=current_user.id,
                category_id=category_id
            )

            db.session.add(new_txn)
            db.session.commit()

            flash("Transaction added successfully!", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding transaction: {str(e)}", "danger")

    return render_template("add_transaction.html", categories=categories)