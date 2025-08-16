from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaction, Category

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/transactions", methods=["GET", "POST"])
@login_required
def index():
    uid = current_user.id
    categories = db.session.query(Category).filter_by(user_id=uid).order_by(Category.name).all()

    if request.method == "POST":
        t_type = request.form["type"]
        amount = request.form["amount"]
        desc = request.form.get("description", "")
        t_date_str = request.form.get("date") or date.today().isoformat()
        cat_id = request.form.get("category_id") or None

        # ✅ Convert string → Python date
        try:
            t_date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        except ValueError:
            t_date = date.today()

        if t_type not in ("income", "expense"):
            flash("Invalid type.", "danger")
            return redirect(url_for("transactions.index"))

        tx = Transaction(
            user_id=uid,
            category_id=int(cat_id) if cat_id else None,
            amount=float(amount),
            type=t_type,
            description=desc,
            date=t_date
        )
        db.session.add(tx)
        db.session.commit()
        flash("Transaction added.", "success")
        return redirect(url_for("transactions.index"))

    q = db.session.query(Transaction).filter_by(user_id=uid).order_by(Transaction.date.desc(), Transaction.id.desc())
    transactions = q.all()
    return render_template("transactions.html", transactions=transactions, categories=categories, today=date.today())


@transactions_bp.route("/transactions/<int:tx_id>/delete", methods=["POST"])
@login_required
def delete(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.user_id != current_user.id:
        flash("Not found.", "warning")
        return redirect(url_for("transactions.index"))
    db.session.delete(tx)
    db.session.commit()
    flash("Deleted.", "success")
    return redirect(url_for("transactions.index"))


@transactions_bp.route("/transactions/<int:tx_id>/edit", methods=["POST"])
@login_required
def edit(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if not tx or tx.user_id != current_user.id:
        flash("Not found.", "warning")
        return redirect(url_for("transactions.index"))

    tx.type = request.form.get("type", tx.type)
    tx.amount = float(request.form.get("amount", tx.amount))
    tx.description = request.form.get("description", tx.description)

    # ✅ Handle date conversion
    t_date_str = request.form.get("date")
    if t_date_str:
        try:
            tx.date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    cat_id = request.form.get("category_id")
    tx.category_id = int(cat_id) if cat_id else None

    db.session.commit()
    flash("Updated.", "success")
    return redirect(url_for("transactions.index"))
