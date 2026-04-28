"""
notifier.py
-----------
Notification utility for sending messages via Discord webhook, email, or stdout.
"""

import logging

class Notifier:
	"""
	Sends notifications to Discord, email, or stdout based on config.
	"""
	def __init__(self, config: dict) -> None:
		"""
		Initialize Notifier with configuration.
		Args:
			config: Dictionary with notification settings (e.g., discord_webhook, email).
		"""
		self.config = config

	def notify(self, message: str) -> None:
		"""
		Send a notification message using the configured method.
		Args:
			message: The message to send.
		"""
		if self.config.get('discord_webhook'):
			import requests
			# Send message to Discord webhook
			try:
				requests.post(self.config['discord_webhook'], json={"content": message})
			except Exception as e:
				logging.error(f"Failed to send Discord notification: {e}")
		elif self.config.get('email'):
			# Send email notification using SMTP
			try:
				import smtplib
				from email.message import EmailMessage
				email_cfg = self.config['email']
				msg = EmailMessage()
				msg.set_content(message)
				msg['Subject'] = email_cfg.get('subject', 'useget Notification')
				msg['From'] = email_cfg['from']
				msg['To'] = email_cfg['to']
				with smtplib.SMTP(email_cfg['smtp_server'], email_cfg.get('smtp_port', 587)) as server:
					server.starttls()
					server.login(email_cfg['username'], email_cfg['password'])
					server.send_message(msg)
				logging.info(f"Email sent to {email_cfg['to']}")
			except Exception as e:
				logging.error(f"Failed to send email notification: {e}")
		else:
			# Fallback: log to stdout
			logging.info(f"NOTIFY: {message}")
