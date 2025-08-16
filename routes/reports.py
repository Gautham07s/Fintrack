from flask import Blueprint, render_template, request, send_file, flash
from flask_login import login_required, current_user
from io import BytesIO
import pandas as pd
from models import db, Transaction, Category
from utils import df_to_csv_bytes, simple_pdf_bytes

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports")
@login_required
def view():
    uid = current_user.id
    start = request.args.get("start")
    end = request.args.get("end")
    cat = request.args.get("category", "all")

    q = db.session.query(Transaction).filter(Transaction.user_id == uid)
    if start: q = q.filter(Transaction.date >= start)
    if end:   q = q.filter(Transaction.date <= end)
    if cat and cat != "all":
        c = db.session.query(Category).filter_by(user_id=uid, name=cat).first()
        q = q.filter(Transaction.category_id == (c.id if c else -1))

    rows = q.order_by(Transaction.date.desc()).all()
    categories = db.session.query(Category).filter_by(user_id=uid).order_by(Category.name).all()
    return render_template("reports.html", rows=rows, categories=categories, start=start or "", end=end or "", sel_cat=cat)

@reports_bp.route("/reports/export/<fmt>")
@login_required
def export(fmt):
    uid = current_user.id
    start = request.args.get("start")
    end = request.args.get("end")
    cat = request.args.get("category", "all")

    q = db.session.query(Transaction).filter(Transaction.user_id == uid)
    if start: q = q.filter(Transaction.date >= start)
    if end:   q = q.filter(Transaction.date <= end)
    if cat and cat != "all":
        c = db.session.query(Category).filter_by(user_id=uid, name=cat).first()
        q = q.filter(Transaction.category_id == (c.id if c else -1))

    data = [{
        "Date": r.date.isoformat(),
        "Type": r.type,
        "Category": (r.category.name if r.category else ""),
        "Amount": float(r.amount),
        "Description": r.description or ""
    } for r in q.order_by(Transaction.date).all()]

    df = pd.DataFrame(data)
    if fmt == "csv":
        return send_file(BytesIO(df_to_csv_bytes(df)), as_attachment=True,
                         download_name="fintrack_report.csv", mimetype="text/csv")
    if fmt == "pdf":
        lines = [f"{d['Date']} | {d['Type']:7} | {(d['Category'] or '-'):12} | {d['Amount']:>10} | {d['Description']}" for d in data]
        return send_file(BytesIO(simple_pdf_bytes("FinTrack Report", lines)), as_attachment=True,
                         download_name="fintrack_report.pdf", mimetype="application/pdf")
    flash("Unsupported format.", "warning")
    return view()
