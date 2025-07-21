from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)  # allow cross-origin requests

# Endpoint for grading (optional, you can do grading on frontend)
@app.route('/api/grade', methods=['POST'])
def grade():
    data = request.json
    score = data.get('score')
    try:
        score = float(score)
        if not (0 <= score <= 100):
            return jsonify({"error": "Invalid score"}), 400
    except:
        return jsonify({"error": "Invalid input"}), 400

    if score >= 70:
        grade = "A"
    elif score >= 60:
        grade = "B"
    elif score >= 50:
        grade = "C"
    elif score >= 45:
        grade = "D"
    elif score >= 40:
        grade = "E"
    else:
        grade = "F"

    return jsonify({"grade": grade})

# Endpoint to send mail - e.g. request docs (you can call this from frontend)
@app.route('/api/send-mail', methods=['POST'])
def send_mail():
    data = request.json
    to_email = data.get('to_email')
    subject = data.get('subject', 'EduPulse Mail')
    body = data.get('body', '')

    # NOTE: Use environment variables or secure config for real credentials
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
