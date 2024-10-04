import os
from dotenv import load_dotenv, find_dotenv

class ConfigLoader:
    def __init__(self):
        print("ConfigLoader.__init__")

        # Automatically load the .env file if it exists
        dotenv_path = find_dotenv()
        if dotenv_path:
            load_dotenv(dotenv_path)
        
        try:
            self.keys = {
                "hermes_key": self._get_env_var("HERMES_KEY"),
                "slack_event_key": self._get_env_var("SLACK_EVENT_KEY"),
                "slack_command_key": self._get_env_var("SLACK_COMMAND_KEY"),
                "api_command_key": self._get_env_var("API_COMMAND_KEY")
            }
            self.nextcloud = {
                "username": self._get_env_var("NEXTCLOUD_USERNAME"),
                "token": self._get_env_var("NEXTCLOUD_ACCESS_TOKEN"),
                "url": self._get_env_var("NEXTCLOUD_URL"),
                "path": self._get_env_var("NEXTCLOUD_PATH")
            }
            self.dropbox = {
                "token": self._get_env_var("DROPBOX_ACCESS_TOKEN")
            }
            self.slack = {
                "token": self._get_env_var("SLACK_TOKEN"),
                "channel": self._get_env_var("DEFAULT_SLACK_CHANNEL")
            }
            self.hermes = {
                "device_types": self._get_env_var("DEVICE_TYPES").split(","),
                "prefixes": self._get_env_var("PREFIXES").split(","),
                "port":self._get_env_var("PORT")
            }

        except Exception as e:
            print(f"Error loading config: {e}")

    def _get_env_var(self, var_name):
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Missing required environment variable: {var_name}")
        return value
