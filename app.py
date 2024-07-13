from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import logging

app = Flask(__name__)

# 设置日志记录
logging.basicConfig(filename="app.log", level=logging.DEBUG)


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
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


@app.route("/send_email", methods=["POST"])
def handle_send_email():
    data = request.form
    sender_email = data.get("sender_email")
    sender_password = data.get("sender_password")
    recipient_email = data.get("recipient_email")
    email_subject = data.get("subject")

    if "body_file" in request.files:
        body_file = request.files["body_file"]
        email_body = body_file.read().decode("utf-8")
        logging.debug(f"Email body: {email_body}")
    else:
        email_body = "No body file provided."

    try:
        send_email(
            sender_email, sender_password, recipient_email, email_subject, email_body
        )
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 400


@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        with open("app.log", "r") as file:
            logs = file.readlines()
        logs_formatted = "<pre>" + "<br>".join(logs) + "</pre>"
        return logs_formatted, 200
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
