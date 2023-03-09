import json


class ConfigLoader:
    def __init__(self, config_file):
        print("ConfigLoader.__init__")
        try:
            config = json.load(open(config_file))
            self.keys = {
                "hermes_key": config["hermes_key"],
                "slack_event_key": config["slack_event_key"],
                "slack_command_key": config["slack_command_key"]
            }
            self.nextcloud = {
                "username": config["nextcloud_username"],
                "token": config["nextcloud_access_token"],
                "url": config["nextcloud_url"]
            }
            self.dropbox = {
                "token": config["dropbox_access_token"]
            }
            self.slack = {
                "token": config["slack_token"],
                "channel": config["default_slack_channel"]
            }
            self.hermes = {
                "device_types": config["device_types"],
                "prefixes": config["prefixes"]
            }
        except FileNotFoundError as e:
            print(f"Error loading config from {config_file}: {e}")
        except Exception as e:
            print(f"Error loading config: {e}")

