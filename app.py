import os
from flask import Flask, jsonify, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True  # Important: Set to True if using TLS
app.config["MAIL_USE_SSL"] = False  # Set to False if using TLS
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

mail = Mail(app)

@app.route('/forward', methods=['POST']) 
def forward_email():
    try:
        data = request.get_json()

        subject = data.get('subject')
        message = data.get('message')
        sender_email = data.get('sender_email')

        if not all([subject, message, sender_email]):
            return jsonify({'error': 'Missing required fields'}), 400

        msg = Message(
            subject,
            sender= os.environ.get("MAIL_USERNAME"),  # Sender is the original sender
            recipients=[os.environ.get("MAIL_USERNAME")]
        )
        msg.body = message+f"\nSent by {sender_email}"  # Set the message body

        mail.send(msg)
        return jsonify({'message': 'Email forwarded successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)


