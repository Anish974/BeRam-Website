# test_mail.py
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object('config.Config')
mail = Mail(app)

with app.app_context():
    msg = Message('Test Email', recipients=['your-email@example.com'])
    msg.body = 'This is a test email'
    try:
        mail.send(msg)
        print('Mail sent successfully')
    except Exception as e:
        print('Mail sending failed:', e)
