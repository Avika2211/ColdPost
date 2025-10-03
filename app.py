from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/')
def index():
    return send_from_directory('.', 'sender.html')  # Serve your frontend

@app.route('/send-emails', methods=['POST'])
def send_emails():
    try:
        # Get form data (multipart/form-data)
        sender_email = request.form['senderEmail']
        sender_password = request.form['senderPassword']
        subject = request.form['subject']
        template = request.form['template']
        recipients = json.loads(request.form['recipients'])  # Recipients sent as JSON string
        
        # Get attachments
        attachments = request.files.getlist('attachments')

        results = []
        failed = []

        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient in recipients:
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient['email']
                msg['Subject'] = subject

                # Personalize message
                personalized_body = template.replace('{name}', recipient['name'])
                msg.attach(MIMEText(personalized_body, 'plain'))

                # Attach files
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={attachment.filename}')
                    msg.attach(part)
                    attachment.seek(0)  # Reset file pointer for next recipient

                server.send_message(msg)
                results.append({
                    'name': recipient['name'],
                    'email': recipient['email'],
                    'status': 'success'
                })
            except Exception as e:
                failed.append({
                    'name': recipient['name'],
                    'email': recipient['email'],
                    'error': str(e)
                })

        server.quit()

        return jsonify({
            'success': True,
            'sent': len(results),
            'failed': len(failed),
            'results': results,
            'failures': failed
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Server starting on http://localhost:5000")
    app.run(debug=True, port=5000)
