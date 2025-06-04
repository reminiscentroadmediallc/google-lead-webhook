from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

EMAIL_TO = "info@reminiscentroadmedia.com"
EMAIL_FROM = os.environ.get("SMTP_USERNAME")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

@app.route("/google-lead-webhook", methods=["POST"])
def receive_lead():
    data = request.get_json()

    message = "New Google Lead Received:\n\n"
    for key, value in data.items():
        message += f"{key}: {value}\n"

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