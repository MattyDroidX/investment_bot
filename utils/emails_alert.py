# utils/email_alerts.py
import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "YOUR_EMAIL"
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("YOUR_EMAIL", "YOUR_PASSWORD")
        smtp.send_message(msg)
