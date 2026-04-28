"""
notifier.py
-----------
Notification utility for sending messages via Discord webhook, email, or stdout.
"""

class Notifier:
	"""
	Sends notifications to Discord, email, or stdout based on config.
	"""
	def __init__(self, config):
		# config: dict with notification settings (e.g., discord_webhook, email)
		self.config = config

	def notify(self, message):
		"""
		Send a notification message using the configured method.
		"""
		if self.config.get('discord_webhook'):
			import requests
			# Send message to Discord webhook
			requests.post(self.config['discord_webhook'], json={"content": message})
		elif self.config.get('email'):
			# Placeholder: implement email notification
			print(f"Email: {message}")
		else:
			# Fallback: print to stdout
			print(f"NOTIFY: {message}")
