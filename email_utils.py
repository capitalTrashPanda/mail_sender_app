import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from loguru import logger


def is_valid_recipient(email):
    return re.match(r"^[^@]+@gmail\.com$", email)


def send_email(sender, password, recipient, subject, body):
    if not is_valid_recipient(recipient):
        raise ValueError("Invalid recipient address")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        logger.debug("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
