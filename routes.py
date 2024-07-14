from flask import Flask, request, jsonify
from loguru import logger
from email_utils import send_email
from models import session, LogEntry

app = Flask(__name__)


@app.route("/send_email", methods=["POST"])
def handle_send_email():
    data = request.form
    sender_email = data.get("sender_email")
    sender_password = data.get("sender_password")
    recipient_email = data.get("recipient_email")
    email_subject = data.get("subject")

    logger.debug(f"Subject: {email_subject}")
    logger.debug(f"Sender: {sender_email}")
    logger.debug(f"Recipient: {recipient_email}")

    if "body_file" in request.files:
        body_file = request.files["body_file"]
        email_body = body_file.read().decode("utf-8")
    else:
        email_body = "No body file provided."

    try:
        send_email(
            sender_email, sender_password, recipient_email, email_subject, email_body
        )
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        log_entries = session.query(LogEntry).all()
        logs_formatted = ""
        for entry in log_entries:
            logs_formatted += (
                f"<pre>{entry.timestamp} - {entry.level} - {entry.message}</pre><br>"
            )
        return logs_formatted, 200
    except Exception as e:
        return str(e), 500
