import io
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    return buf.getvalue().encode("utf-8")

def simple_pdf_bytes(title: str, lines: list[str]) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    c.setFont("Helvetica", 11)
    y -= 30
    for line in lines or ["No records found."]:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(50, y, line)
        y -= 18
    c.save()
    buffer.seek(0)
    return buffer.read()
