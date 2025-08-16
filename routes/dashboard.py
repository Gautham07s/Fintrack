from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func, case
from models import db, Transaction, Category

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def home():
    uid = current_user.id

    totals = db.session.query(
        func.coalesce(func.sum(case((Transaction.type=='income', Transaction.amount), else_=0)), 0).label("income"),
        func.coalesce(func.sum(case((Transaction.type=='expense', Transaction.amount), else_=0)), 0).label("expense")
    ).filter(Transaction.user_id==uid).one()
    balance = float(totals.income or 0) - float(totals.expense or 0)

    # Category-wise expenses
    cat_rows = db.session.query(Category.name, func.coalesce(func.sum(Transaction.amount), 0)) \
        .join(Transaction, Transaction.category_id==Category.id, isouter=True) \
        .filter(Category.user_id==uid, Transaction.type=='expense') \
        .group_by(Category.name).all()
    cat_labels = [r[0] for r in cat_rows if float(r[1] or 0) > 0]
    cat_values = [float(r[1]) for r in cat_rows if float(r[1] or 0) > 0]

    # Monthly trend (SQLite vs Postgres)
    sql = """
        SELECT strftime('%Y-%m-01', date) AS month, SUM(amount) AS total
        FROM transactions
        WHERE user_id = :uid AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """ if db.engine.url.get_backend_name().startswith("sqlite") else """
        SELECT date_trunc('month', date) AS month, SUM(amount) AS total
        FROM transactions
        WHERE user_id = :uid AND type = 'expense'
        GROUP BY month
        ORDER BY month
    """
    trend_rows = db.session.execute(db.text(sql), {"uid": uid}).fetchall()
    trend_labels = [str(r[0])[:10] for r in trend_rows]
    trend_values = [float(r[1]) for r in trend_rows]

    return render_template("dashboard.html",
                           income=float(totals.income or 0),
                           expense=float(totals.expense or 0),
                           balance=balance,
                           cat_labels=cat_labels, cat_values=cat_values,
                           trend_labels=trend_labels, trend_values=trend_values)
