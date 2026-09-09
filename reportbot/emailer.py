import smtplib
from email.message import EmailMessage
from pathlib import Path
from .config import SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, SMTP_HOST, SMTP_PORT, SEND_EMAIL

def send_report(pdf_path: Path, metrics: dict):
    if not SEND_EMAIL:
        return False, "Email sending disabled (REPORTBOT_SEND_EMAIL=false)."

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        raise RuntimeError("Email is enabled but SMTP credentials/recipient are missing.")

    msg = EmailMessage()
    msg["Subject"] = "ReportBot — Automated Sales Analytics Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg.set_content(
        f"ReportBot completed the sales analysis.\n\n"
        f"Revenue: ₹{metrics['total_revenue']:,.0f}\n"
        f"Orders: {metrics['orders']:,}\n"
        f"AOV: ₹{metrics['aov']:,.0f}\n"
        f"MoM Growth: {metrics['mom_growth']:.2f}%\n\n"
        "The full PDF report is attached."
    )
    msg.add_attachment(pdf_path.read_bytes(), maintype="application", subtype="pdf", filename=pdf_path.name)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)

    return True, "Email sent successfully."

def send_with_retry(pdf_path, metrics, attempts=3):
    last_error = None
    for _ in range(attempts):
        try:
            return send_report(pdf_path, metrics)
        except Exception as exc:
            last_error = exc
    raise last_error
