import os

ENV_PREFIX = os.getenv("ENV_PREFIX", "")

def getenv(value, default=None):
  return os.getenv(ENV_PREFIX + value, default)

SLACK_TOKEN = getenv("SLACK_TOKEN")
SLACK_USERNAME = getenv("SLACK_USERNAME")
SLACK_CHANNEL = getenv("SLACK_CHANNEL", "#olark")
SLACK_PRESENCE_INTERVAL = int(getenv("SLACK_PRESENCE_INTERVAL", 60))
SLACK_NOTIFICATION_INTERVAL = int(getenv("SLACK_NOTIFICATION_INTERVAL", 360))

OLARK_USERNAME = getenv("OLARK_USERNAME")
OLARK_PASSWORD = getenv("OLARK_PASSWORD")
OLARK_XMPP_HOST = getenv("OLARK_XMPP_HOST", "olark.com")
OLARK_XMPP_PORT = int(getenv("OLARK_XMPP_PASSWORD", 5222))
OLARK_WEBSERVICE_URL = getenv("OLARK_WEBSERVICE_URL", "https://chat.olark.com")
OLARK_IGNORE_USERS = getenv("OLARK_IGNORE_USERS", "").split(",")