from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

app = Flask(__name__)


def is_valid_recipient(email):
    return re.match(r"^[^@]+@gmail\.com$", email)


def read_email_body(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


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
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route("/send_email", methods=["POST"])
def handle_send_email():
    data = request.json
    sender_email = data.get("sender_email")
    sender_password = data.get("sender_password")
    recipient_email = data.get("recipient_email")
    email_subject = data.get("subject")
    email_body_file = data.get("body_file")

    try:
        email_body = read_email_body(email_body_file)
        send_email(
            sender_email, sender_password, recipient_email, email_subject, email_body
        )
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(port=5000, debug=True)
