from flask import current_app
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
	current_app.logger.info("send_async email...")
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	#mail.send(msg)
	current_app.logger.info("send email...")
	Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

