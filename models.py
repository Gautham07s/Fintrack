from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    categories = db.relationship("Category", backref="user", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", backref="user", cascade="all, delete-orphan")

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = db.Column(db.String(50), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='uq_user_category'),)

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False, default=date.today)
    category = db.relationship("Category", lazy="joined")
