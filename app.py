from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Load email credentials and recipient
EMAIL_TO = "info@reminiscentroadmedia.com"
EMAIL_FROM = os.environ.get("SMTP_USERNAME")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
EXPECTED_KEY = os.environ.get("GOOGLE_WEBHOOK_KEY")

@app.route("/google-lead-webhook", methods=["POST"])
def receive_lead():
    # Validate content type
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"status": "invalid content type"}), 400

    data = request.get_json()
    if not data or "user_column_data" not in data:
        return jsonify({"status": "invalid payload"}), 400

    # Optional header key check (adjust if needed)
    received_key = request.headers.get("X-Goog-Signature")
    if EXPECTED_KEY and received_key != EXPECTED_KEY:
        return jsonify({"status": "unauthorized"}), 403

    # Build the message
    message = "New Google Lead Received:\n\n"
    for field in data.get("user_column_data", []):
        message += f"{field.get('column_name')}: {field.get('string_value')}\n"

    # Send the email
    try:
        msg = MIMEText(message)
        msg['Subject'] = "New Google Lead Form Submission"
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)