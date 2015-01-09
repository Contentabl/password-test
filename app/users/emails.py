from flask.ext.mail import Message
from app import mail
from app.users.models import *
from config import *

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	mail.send(msg)

from flask import render_template

def send_all_emails():
	emails = []
	users = User.query.all()
	for user in users:
		emails.append(user.email)
	print SITE_URL
	#send_email("Meals to Heal for this week", MAIL_USERNAME, emails, 
	#	render_template('weeklyemail.txt', url = SITE_URL), render_template('weeklyemail.html', url = SITE_URL))	