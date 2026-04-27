class Notifier:
    def __init__(self, config):
        self.config = config

    def notify(self, message):
        if self.config.get('discord_webhook'):
            import requests
            requests.post(self.config['discord_webhook'], json={"content": message})
        elif self.config.get('email'):
            # Placeholder: implement email notification
            print(f"Email: {message}")
        else:
            print(f"NOTIFY: {message}")
